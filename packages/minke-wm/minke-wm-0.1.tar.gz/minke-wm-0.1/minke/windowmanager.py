import Xlib.rdb
import Xlib.XK
import struct
import os
import sys
import resource
import math
import itertools

MAX_EXCEPTIONS = 25
BORDER_WIDTH = 4
BORDER_COLOUR = 0xF92672

class Workspace:
    def __init__(self, name):
        self.name = name
        self.layouts = [
                SpiralLayout(),
                VerticalLayout(),
                HorizontalLayout(),
                TallLayout(),
                ThreeColLayout(),
                FullLayout(),
                ]
        self.windows = []
        self.focus_index = 0

    def __repr__(self):
        return f'minke.windowmanager.Workspace(name={self.name})'

    def main_window_larger(self, root):
        self.layouts[0].main_window_larger()
        self.do_layout(root)

    def main_window_smaller(self, root):
        self.layouts[0].main_window_smaller()
        self.do_layout(root)

    def hide(self):
        for w in self.windows:
            w.unmap()

    def show(self):
        for w in self.windows:
            w.map()

    def close_focused(self):
        try:
            self.windows[self.focus_index].destroy()
        except IndexError:
            pass

    def remove_window(self, window):
        try:
            window_index = self.windows.index(window)
            if window_index < self.focus_index and self.focus_index > 0:
                self.focus_index -= 1
            self.windows.remove(window)
            if self.focus_index >= len(self.windows):
                self.focus_index = len(self.windows) - 1
        except ValueError:
            pass

    def add_window(self, window):
        self.windows.append(window)
        self.focus_index = len(self.windows) - 1


    def cycle_focus(self):
        self.focus_index += 1
        if self.focus_index >= len(self.windows):
            self.focus_index = 0
        self.render_focus()

    def reverse_cycle_focus(self):
        self.focus_index -= 1
        if self.focus_index < 0:
            self.focus_index =  len(self.windows) - 1
        self.render_focus()

    def render_focus(self):
        try:
            self.windows[self.focus_index].set_input_focus(
                    revert_to=Xlib.X.RevertToParent,
                    time=Xlib.X.CurrentTime)
            self.windows[self.focus_index].configure(stack_mode=Xlib.X.Above)
            for window in self.windows:
                window.change_attributes(border_pixel=0x888888)
            self.windows[self.focus_index].change_attributes(
                    border_pixel=BORDER_COLOUR)
        except IndexError:
            # no windows
            pass

    def do_layout(self, root):
        self.layouts[0].layout(self.windows, root.get_geometry())
        if self.windows:
            self.windows[self.focus_index].set_input_focus(
                    revert_to=Xlib.X.RevertToParent,
                    time=Xlib.X.CurrentTime)
            self.windows[self.focus_index].configure(stack_mode=Xlib.X.Above)

    def cycle_layout(self):
        self.layouts = self.layouts[1:] + self.layouts[:1]

    def down_window_order(self):
        if self.focus_index == 0:
            self.windows = self.windows[1:] + self.windows[:1]
            self.focus_index = len(self.windows) - 1
        else:
            self.windows = self.windows[:self.focus_index - 1] + \
                    [self.windows[self.focus_index]] + \
                    [self.windows[self.focus_index - 1]] + \
                    self.windows[self.focus_index + 1:]
            self.focus_index -= 1

    def up_window_order(self):
        try:
            self.windows = self.windows[:self.focus_index] + \
                    [self.windows[self.focus_index + 1]] + \
                    [self.windows[self.focus_index]] + \
                    self.windows[self.focus_index + 2:]
            self.focus_index += 1
        except IndexError:
            self.windows = [self.windows[self.focus_index]] + \
                    self.windows[:self.focus_index]
            self.focus_index = 0


class WindowManager:
    def __init__(self):
        self.display, appname, self.resource_db, args = \
                Xlib.rdb.get_display_opts(Xlib.rdb.stdopts)
        # Hotkeys
        self.hotkeys = {
                Xlib.XK.XK_Return: self.new_terminal,
                Xlib.XK.XK_t: self.tile_windows,
                Xlib.XK.XK_space: self.cycle_layout,
                Xlib.XK.XK_Tab: self.cycle_focus,
                Xlib.XK.XK_j: self.down_window_order,
                Xlib.XK.XK_k: self.up_window_order,
                Xlib.XK.XK_p: self.dmenu,
                Xlib.XK.XK_c: self.close,
                Xlib.XK.XK_h: self.main_window_smaller,
                Xlib.XK.XK_l: self.main_window_larger,
                }

        self.hotkeys_shift = {
                Xlib.XK.XK_Tab: self.reverse_cycle_focus,
                }

        # Workspaces
        workspace_keysyms = [
                Xlib.XK.XK_1,
                Xlib.XK.XK_2,
                Xlib.XK.XK_3,
                Xlib.XK.XK_4,
                Xlib.XK.XK_5,
                Xlib.XK.XK_6,
                Xlib.XK.XK_7,
                Xlib.XK.XK_8,
                Xlib.XK.XK_9,
                ]
        self.workspaces_by_keycode = {}
        self.active_workspace = None
        for n, ks in zip(itertools.count(1), workspace_keysyms):
            self.hotkeys[ks] = self.switch_workspace
            self.hotkeys_shift[ks] = self.move_to_workspace
            workspace = Workspace(n)
            if self.active_workspace is None:
                self.active_workspace = workspace
            for kc in {code for code, i in self.display.keysym_to_keycodes(ks)}:
                self.workspaces_by_keycode[kc] = workspace

        # map key symbols to key codes
        self.hotkey_shift_codes = [
                ({code for code, index in self.display.keysym_to_keycodes(key)},
                handler) for key, handler in self.hotkeys_shift.items()]
        self.hotkey_codes = [
                ({code for code, index in self.display.keysym_to_keycodes(key)},
                handler) for key, handler in self.hotkeys.items()]

        self.screens = [screen_id for screen_id
                in range(0, self.display.screen_count())
                if self.redirect_screen_events(screen_id)]

        self.display.set_error_handler(self.x_error_handler)

        self.event_dispatcher = {
                Xlib.X.KeyPress: self.handle_key_press,
                Xlib.X.KeyRelease: self.handle_key_release,
                Xlib.X.ConfigureRequest: self.handle_configure_request,
                Xlib.X.MapRequest: self.handle_map_request,
                Xlib.X.MapNotify: self.handle_map_notify,
                Xlib.X.UnmapNotify: self.handle_unmap_notify,
                Xlib.X.DestroyNotify: self.handle_destroy_notify,
                }

    def x_error_handler(self, error, request):
        print(f'X Protocol Error {error}', file=sys.stderr)

    def redirect_screen_events(self, screen_id):
        root = self.display.screen(screen_id).root
        error_catcher = Xlib.error.CatchError(Xlib.error.BadAccess)
        root.change_attributes(
                event_mask=Xlib.X.SubstructureRedirectMask |
                            Xlib.X.SubstructureNotifyMask,
                onerror=error_catcher)
        self.display.sync()
        if error_catcher.get_error():
            return False

        for key in self.hotkeys_shift.keys():
            codes = {code for code, index in
                    self.display.keysym_to_keycodes(key)}
            for code in codes:
                root.grab_key(
                        code,
                        Xlib.X.Mod1Mask | Xlib.X.ShiftMask,
                        1,
                        Xlib.X.GrabModeAsync,
                        Xlib.X.GrabModeAsync)

        for key in self.hotkeys.keys():
            codes = {code for code, index in
                    self.display.keysym_to_keycodes(key)}
            for code in codes:
                root.grab_key(
                        code,
                        Xlib.X.Mod1Mask & ~(Xlib.X.AnyModifier << 1),
                        1,
                        Xlib.X.GrabModeAsync,
                        Xlib.X.GrabModeAsync)

        # Find all existing windows.
        for window in root.query_tree().children:
            # TODO make this per-screen_id
            self.active_workspace.add_window(window)
        self.do_layout(root)

        return True

    def main_loop(self):
        exception_count = 0
        while True:
            try:
                print('main_loop: handle event...')
                self.handle_event()
                print('main_loop: event handled.')
            except (KeyboardInterrupt, SystemExit):
                raise
            #except:
                #exception_count += 1
                #if exception_count > MAX_EXCEPTIONS:
                    #raise

    def handle_event(self):
        try:
            event = self.display.next_event()
        except Xlib.error.ConnectionClosedError:
            raise KeyboardInterrupt

        try:
            self.event_dispatcher[event.type](event)
        except KeyError:
            print('handle_event, unhandled:', event)

    # Event handlers
    def handle_configure_request(self, event):
        args = {'border_width': BORDER_WIDTH}
        if event.value_mask & Xlib.X.CWX:
            args['x'] = event.x
        if event.value_mask & Xlib.X.CWY:
            args['y'] = event.y
        if event.value_mask & Xlib.X.CWWidth:
            args['width'] = event.width
        if event.value_mask & Xlib.X.CWHeight:
            args['height'] = event.height
        if event.value_mask & Xlib.X.CWSibling:
            args['sibling'] = event.above
        if event.value_mask & Xlib.X.CWStackMode:
            args['stack_mode'] = event.stack_mode
        event.window.configure(**args)

    def handle_map_request(self, event):
        event.window.map()
        self.active_workspace.add_window(event.window)

    def handle_map_notify(self, event):
        print('handle_map_notify:')
        self.do_layout(event.window.query_tree().root)
        self.render_focus()

    def handle_unmap_notify(self, event):
        pass

    def handle_destroy_notify(self, event):
        print('handle_destroy_notify:')
        self.active_workspace.remove_window(event.window)
        self.do_layout(event.event)
        self.render_focus()

    def handle_key_press(self, event):
        #print('handle_key_press:', event)
        if event.state & Xlib.X.Mod1Mask and event.state & Xlib.X.ShiftMask:
            for codes, handler in self.hotkey_shift_codes:
                if event.detail in codes:
                    handler(event)
                    break
        elif event.state & Xlib.X.Mod1Mask:
            for codes, handler in self.hotkey_codes:
                if event.detail in codes:
                    handler(event)
                    break

    def handle_key_release(self, event):
        # Intentially empty
        pass

    # Hotkey handlers
    def main_window_smaller(self, event):
        print('main_window_smaller:')
        self.active_workspace.main_window_smaller(event.root)


    def main_window_larger(self, event):
        print('main_window_larger:')
        self.active_workspace.main_window_larger(event.root)

    def close(self, event):
        print('close:', event)
        self.active_workspace.close_focused()

    def switch_workspace(self, event):
        print('switch_workspace:')
        workspace = self.workspaces_by_keycode[event.detail]
        self.active_workspace.hide()
        self.active_workspace = workspace
        self.active_workspace.show()
        self.do_layout(event.root)
        self.render_focus()

    def move_to_workspace(self, event):
        print('move_to_workspace:')
        self.active_workspace.hide()
        to_workspace = self.workspaces_by_keycode[event.detail]
        to_workspace.add_window(event.child)
        self.active_workspace.remove_window(event.child)
        self.active_workspace.show()
        self.do_layout(event.root)
        self.render_focus()

    def new_terminal(self, event):
        print('new_terminal:')
        #self.spawn(['/usr/local/bin/st'])
        #self.spawn(['/usr/bin/rxvt'])
        self.spawn(['/usr/bin/xterm'])

    def dmenu(self, event):
        self.spawn(['/usr/bin/dmenu_run'])

    def spawn(self, command):
        if os.fork() != 0:
            return # parent
        # child
        try:
            os.setsid()
            if os.fork() !=0:
                os._exit(0) # child terminates
            # grandchild
            os.chdir(os.path.expanduser('~'))
            os.umask(0)
            maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
            if maxfd == resource.RLIM_INFINITY:
                maxfd = 1024
            for fd in range(maxfd):
                try:
                    os.close(fd)
                except OSError:
                    pass
            os.open('/dev/null', os.O_RDWR)
            os.dup2(0, 1)
            os.dup2(0, 2)
            os.execve(command[0], command, os.environ)
        except:
            print('Error in child process', file=sys.stderr)
            sys.exit(1)

    def cycle_focus(self, event):
        print('cycle_focus:')
        self.active_workspace.cycle_focus()

    def reverse_cycle_focus(self, event):
        print('reverse_cycle_focus:')
        self.active_workspace.reverse_cycle_focus()

    def render_focus(self):
        self.active_workspace.render_focus()

    def tile_windows(self, event):
        print('tile_windows:', event)
        self.do_layout(event.root)
        self.render_focus()

    def do_layout(self, root):
        self.active_workspace.do_layout(root)

    def cycle_layout(self, event):
        print('cycle_layout:')
        self.active_workspace.cycle_layout()
        self.do_layout(event.root)

    def down_window_order(self, event):
        print('down_window_order:')
        self.active_workspace.down_window_order()
        self.do_layout(event.root)

    def up_window_order(self, event):
        self.active_workspace.up_window_order()
        self.do_layout(event.root)


class Layout:
    borders = 2 * BORDER_WIDTH
    
    def main_window_larger(self):
        pass

    def main_window_smaller(self):
        pass


class VerticalLayout(Layout):
    def layout(self, windows, root_geometry):
        if windows:
            y=0
            window_height = math.floor(root_geometry.height / len(windows))
            for window in windows:
                window.configure(x=0, y=y,
                        width=root_geometry.width - self.borders,
                        height=window_height - self.borders)
                y += window_height


class HorizontalLayout(Layout):
    def layout(self, windows, root_geometry):
        if windows:
            x=0
            window_width = math.floor(root_geometry.width / len(windows))
            for window in windows:
                window.configure(x=x, y=0,
                        width=window_width - self.borders,
                        height=root_geometry.height - self.borders)
                x += window_width


class FullLayout(Layout):
    def layout(self, windows, root_geometry):
        for window in windows:
            window.configure(x=0, y=0,
                    width=root_geometry.width - self.borders,
                    height=root_geometry.height - self.borders)


class TallLayout(FullLayout):
    def __init__(self):
        self.main_window_pc = 50

    def main_window_larger(self):
        self.main_window_pc = min(90, self.main_window_pc + 10)

    def main_window_smaller(self):
        self.main_window_pc = max(10, self.main_window_pc - 10)

    def layout(self, windows, root_geometry):
        if len(windows) < 2:
            super().layout(windows, root_geometry)
        else:
            main_window_width = math.floor(
                    root_geometry.width * self.main_window_pc / 100)
            windows[0].configure(x=0, y=0,
                    width=main_window_width - self.borders,
                    height=root_geometry.height - self.borders)
            y=0
            h2 = math.floor(root_geometry.height / len(windows[1:]))
            for window in windows[1:]:
                window.configure(x=main_window_width, y=y,
                    width=root_geometry.width - main_window_width - self.borders,
                    height=h2 - self.borders)
                y += h2


class ThreeColLayout(Layout):
    def layout(self, windows, root_geometry):
        if windows:
            cols = min(3, len(windows))
            col_width = math.floor(root_geometry.width / cols)
            # column 1
            windows[0].configure(x=0, y=0,
                    width=col_width - self.borders,
                    height=root_geometry.height - self.borders)
            # column 2
            windows_in_col2 = math.ceil(len(windows[1:]) / 2)
            if windows_in_col2:
                y = 0
                h2 = math.floor(root_geometry.height / windows_in_col2)
                for window in windows[1:windows_in_col2 + 1]:
                    window.configure(x=col_width, y=y,
                        width=col_width - self.borders,
                        height=h2 - self.borders)
                    y += h2
                # column 3
                windows_in_col3 = len(windows[windows_in_col2 + 1:])
                if windows_in_col3:
                    y = 0
                    h3 = math.floor(root_geometry.height / windows_in_col3)
                    for window in windows[windows_in_col2 + 1:]:
                        window.configure(x=col_width * 2, y=y,
                            width=col_width - self.borders,
                            height=h3 - self.borders)
                        y += h3


class SpiralLayout(TallLayout):
    def layout(self, windows, root_geometry):
        if len(windows) < 3:
            super().layout(windows, root_geometry)
        else:
            h = root_geometry.height
            w = root_geometry.width
            x = 0
            y = 0
            r = self.main_window_pc / 100
            _windows = list(windows)
            try:
                while _windows:
                    w1 = math.floor(w * r)
                    w2 = w - w1
                    h2 = math.floor(h * r)
                    h3 = h - h2
                    w3 = math.floor(w2 * r)
                    h4 = math.floor(h3 * r)
                    w4 = w2 - w3
                    _windows.pop().configure(x=x, y=y,
                        width=w1 - self.borders,
                        height=h - self.borders)
                    _windows.pop().configure(x=x+w1, y=y,
                        width=w2 - self.borders,
                        height=h2)
                    _windows.pop().configure(x=x+w-w3, y=y+h2,
                        width=w3 - self.borders,
                        height=h3 - self.borders)
                    _windows.pop().configure(x=x+w1, y=y+h-h4,
                        width=w4 - self.borders,
                        height=h4 - self.borders)
                    y = y+h2
                    x = x+w1
                    h = h - h2 - h4
                    w = w - w1 - w3
            except struct.error:
                pass
            except IndexError:
                pass
