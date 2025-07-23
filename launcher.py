import flet as ft
import os
import asyncio
import random
from math import pi
import subprocess
import sys
import totem

PROFILE_FILE = "profile.txt"

def main(page: ft.Page):
    page.title = "Totem Lite"
    page.bgcolor = ft.colors.BLACK
    page.window.resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {
        "Courier New": "Courier New",
    }
    state = {"nick": None, "avatar": None, "theme": ft.colors.WHITE, "auto_update": True, "selected_version": "1.6"}

    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                parts = f.read().strip().split("|")
                if len(parts) >= 3:
                    state["nick"], state["avatar"] = parts[0], parts[1]
                    state["theme"] = getattr(ft.colors, parts[2], ft.colors.WHITE)
                    if len(parts) >= 4:
                        state["auto_update"] = parts[3].lower() == 'true'
        except Exception as e:
            print(f"Ошибка загрузки профиля: {e}")
            state = {"nick": None, "avatar": None, "theme": ft.colors.WHITE, "auto_update": True, "selected_version": "1.6"}
            if os.path.exists(PROFILE_FILE):
                os.remove(PROFILE_FILE)

    page.window.width = 450
    page.window.height = 720
    page.window.center()

    avatar_file_picker = ft.FilePicker()
    screenshot_file_picker = ft.FilePicker()
    page.overlay.extend([avatar_file_picker, screenshot_file_picker])

    def save_profile():
        theme_name = "WHITE"
        for color_name in dir(ft.colors):
            if color_name.isupper() and getattr(ft.colors, color_name) == state.get('theme'):
                theme_name = color_name
                break
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            f.write(f"{state.get('nick', '')}|{state.get('avatar', '')}|{theme_name}|{state.get('auto_update', True)}")

    def apply_theme():
        page.theme = ft.Theme(
            color_scheme_seed=state["theme"],
            text_theme=ft.TextTheme(body_medium=ft.TextStyle(weight=ft.FontWeight.BOLD))
        )
        page.theme_mode = ft.ThemeMode.DARK
        if hasattr(page, 'main_view_instance') and page.main_view_instance:
            switch_view(get_main_view())
        page.update()

    def center_col(*controls):
        return ft.Container(
            content=ft.Column(
                list(controls),
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True
            ),
            expand=True,
            alignment=ft.alignment.center
        )

    main_content = ft.AnimatedSwitcher(
        content=ft.Container(),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=500,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
        expand=True
    )

    def switch_view(view_control, transition_type=ft.AnimatedSwitcherTransition.FADE):
        main_content.transition = transition_type
        main_content.content = view_control
        main_content.update()

    def get_animation_view():
        size = 25
        gap = 5
        duration = 1000
        theme_color = state["theme"]
        parts = [
            (0, 0, theme_color), (1, 0, theme_color), (2, 0, theme_color), (0, 1, theme_color), (0, 2, theme_color), (1, 2, theme_color), (2, 2, theme_color), (2, 3, theme_color), (0, 4, theme_color), (1, 4, theme_color), (2, 4, theme_color),
            (4, 0, theme_color), (6, 0, theme_color), (4, 1, theme_color), (6, 1, theme_color), (4, 2, theme_color), (6, 2, theme_color), (4, 3, theme_color), (6, 3, theme_color), (4, 4, theme_color), (5, 4, theme_color), (6, 4, theme_color),
            (8, 0, theme_color), (9, 0, theme_color), (10, 0, theme_color), (8, 1, theme_color), (8, 2, theme_color), (10, 2, theme_color), (8, 3, theme_color), (10, 3, theme_color), (8, 4, theme_color), (9, 4, theme_color), (10, 4, theme_color),
            (12, 0, theme_color), (13, 0, theme_color), (14, 0, theme_color), (12, 1, theme_color), (12, 2, theme_color), (14, 2, theme_color), (12, 3, theme_color), (14, 3, theme_color), (12, 4, theme_color), (13, 4, theme_color), (14, 4, theme_color),
            (16, 0, theme_color), (17, 0, theme_color), (18, 0, theme_color), (17, 1, theme_color), (17, 2, theme_color), (17, 3, theme_color), (16, 4, theme_color), (17, 4, theme_color), (18, 4, theme_color),
            (20, 0, theme_color), (22, 0, theme_color), (20, 1, theme_color), (21, 1, theme_color), (20, 2, theme_color), (20, 3, theme_color), (21, 3, theme_color), (20, 4, theme_color), (22, 4, theme_color),
            (25, 0, theme_color), (24, 1, theme_color), (26, 1, theme_color), (24, 2, theme_color), (25, 2, theme_color), (26, 2, theme_color), (24, 3, theme_color), (26, 3, theme_color), (24, 4, theme_color), (26, 4, theme_color),
        ]
        max_col = max(p[0] for p in parts)
        max_row = max(p[1] for p in parts)
        canvas_width = (max_col + 1) * (size + gap) - gap
        canvas_height = (max_row + 1) * (size + gap) - gap
        canvas = ft.Stack(width=canvas_width, height=canvas_height, animate_scale=ft.animation.Animation(duration, ft.AnimationCurve.EASE_IN_OUT), animate_opacity=ft.animation.Animation(duration, ft.AnimationCurve.EASE_IN_OUT))
        for _ in parts:
            canvas.controls.append(ft.Container(width=size, height=size, animate=duration, animate_position=duration, animate_rotation=duration))
        return canvas, parts, canvas_width, canvas_height, duration

    async def run_startup_sequence():
        page.window.width = 1000
        page.window.height = 720
        page.window.center()
        page.update()
        await asyncio.sleep(0.1)
        animation_canvas, parts, canvas_width, canvas_height, duration = get_animation_view()
        all_colors = [ft.colors.AMBER_400, ft.colors.BLUE_400, ft.colors.BROWN_400, ft.colors.CYAN_700, ft.colors.DEEP_ORANGE_500, ft.colors.CYAN_500, ft.colors.INDIGO_600, ft.colors.PINK, ft.colors.RED_600, ft.colors.GREEN_400]
        random.seed()
        for part_container in animation_canvas.controls:
            part_container.left = random.randrange(-100, int(canvas_width) + 100)
            part_container.top = random.randrange(-100, int(canvas_height) + 100)
            part_container.bgcolor = random.choice(all_colors)
            part_container.border_radius = random.randrange(0, 15)
            part_container.rotate = random.randrange(0, 90) * 2 * pi / 360
        animation_canvas.scale = 2
        animation_canvas.opacity = 0.3
        animation_view = center_col(animation_canvas)
        switch_view(animation_view)
        await asyncio.sleep(0.1)
        size = 25
        gap = 5
        theme_color = state["theme"]
        for i, (left, top, _) in enumerate(parts):
            part_container = animation_canvas.controls[i]
            part_container.left = left * (size + gap)
            part_container.top = top * (size + gap)
            part_container.bgcolor = theme_color
            part_container.border_radius = 3
            part_container.rotate = 0
        animation_canvas.scale = 1
        animation_canvas.opacity = 1
        page.update()
        await asyncio.sleep(duration / 1000 + 0.5)
        if state.get("nick") and state.get("avatar"):
            page.window.resizable = True
            switch_view(get_main_view())
        else:
            page.window.width = 450
            page.window.height = 720
            page.window.resizable = False
            page.window.center()
            page.update()
            await asyncio.sleep(0.1)
            switch_view(get_welcome_view())

    async def start_final_step_countdown():
        save_profile()
        switch_view(get_final_view(), ft.AnimatedSwitcherTransition.FADE)
        await asyncio.sleep(2)
        page.window.width = 1000
        page.window.height = 720
        page.window.center()
        page.window.resizable = True
        switch_view(get_main_view(), ft.AnimatedSwitcherTransition.FADE)
    def get_main_view():
        page.main_view_instance = True
        art = r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠉⠛⠿⣿⠅⠈⠀⠁⠀⢽⣿⣿⣿⠀⠁⠈⠀⠁⣿⡿⠛⠉⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢽⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢽⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢽⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣹⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
"""
        def launch_app(e):
            if state.get("selected_version") != "1.6":
                page.open(
                    ft.SnackBar(
                        ft.Text(f"Запуск для версии {state.get('selected_version')} не поддерживается."),
                        bgcolor=ft.colors.RED
                    )
                )
                page.update()
                return

            save_profile()
            page.visible = False
            page.update()

            cmd = [sys.executable, os.path.abspath(__file__), "--run-totem"]


            CREATE_NEW_CONSOLE = 0x00000010
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 3

            try:
                proc = subprocess.Popen(
                    cmd,
                    creationflags=CREATE_NEW_CONSOLE,
                    startupinfo=startupinfo
                )
                result_code = proc.wait()
            except Exception as ex:
                page.visible = True
                page.open(
                    ft.SnackBar(ft.Text(str(ex)), bgcolor=ft.colors.RED)
                )
                page.update()
                return

            if result_code == 100:
                page.visible = True
                page.update()
            else:
                sys.exit(0)


        play_button = ft.Container(
            content=ft.Icon(ft.icons.PLAY_ARROW, size=40, color=ft.colors.WHITE),
            width=80, height=50,
            bgcolor=state["theme"],
            border_radius=15,
            alignment=ft.alignment.center,
            ink=True,
            on_click=launch_app,
            tooltip="Запустить Totem"
        )

        quote_text = "Totem Lite - лаунчер, в котором ты читаешь данное сообщение, предоставляет все бесплатные версии Totem. Полная версия включающая в себя RAT билдер, поиск по 10ТБ баз, фишинг вебки и многое другое находится в Telegram боте."
        telegram_quote = ft.Container(
            content=ft.Stack([
                ft.Container(content=ft.Text(quote_text, color=ft.colors.WHITE, size=14, selectable=True, text_align=ft.TextAlign.CENTER), padding=ft.padding.symmetric(vertical=8, horizontal=25)),
                ft.Container(content=ft.Icon(ft.icons.FORMAT_QUOTE_ROUNDED, color=state["theme"], size=20), top=5, right=5)
            ]),
            width=500, margin=ft.margin.only(top=30, bottom=15), border_radius=10, bgcolor=ft.colors.GREY_900, border=ft.border.all(2, state["theme"])
        )
        
        open_bot_button = ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(ft.icons.TELEGRAM), ft.Text("Открыть бота", weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    style=ft.ButtonStyle(bgcolor=state["theme"], color=ft.colors.WHITE if state["theme"] != ft.colors.WHITE else ft.colors.BLACK, shape=ft.RoundedRectangleBorder(radius=30), padding=ft.padding.symmetric(horizontal=20, vertical=12)),
                    on_click=lambda _: page.launch_url("https://t.me/TotemKmBot"),
                    tooltip="Открыть бота в Telegram",
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

        main_area = ft.Column([
            ft.Container(height=50), 
            ft.Text(art, color=state["theme"], font_family="Courier New", text_align=ft.TextAlign.CENTER),
            ft.Text(f"Привет, {state['nick']}!", color=ft.colors.WHITE, size=24, weight=ft.FontWeight.BOLD),
            telegram_quote,
            ft.Container(expand=True),
            open_bot_button,
            ft.Container(height=30), 
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, expand=True)

        versions_data = {
            "1.0": {"status": "Утеряна", "color": ft.colors.RED, "tooltip": "Версия работает только в Terminal"},
            "1.1": {"status": "Утеряна", "color": ft.colors.RED, "tooltip": "Версия работает только в Terminal"},
            "1.2": {"status": "От 27.06.24", "color": ft.colors.WHITE, "tooltip": "Версия работает только в Terminal"},
            "1.3": {"status": "Утеряна", "color": ft.colors.RED, "tooltip": "Версия работает только в Terminal"},
            "1.4": {"status": "От 14.07.24", "color": ft.colors.WHITE, "tooltip": "Версия работает только в Terminal"},
            "1.5": {"status": "Утеряна", "color": ft.colors.RED, "tooltip": "Версия работает только в Terminal"},
            "1.6": {"status": "От 22.07", "color": ft.colors.WHITE, "tooltip": "Версия работает только в Terminal"}
        }

        versions_menu_column = ft.Column([], spacing=5)
        
        versions_menu = ft.Container(
            content=versions_menu_column,
            width=200, bgcolor=ft.colors.with_opacity(0.9, "#252525"), border=ft.border.all(2, state["theme"]),
            border_radius=10, padding=5, bottom=90, left=20, animate_opacity=ft.animation.Animation(200, "ease"),
            opacity=0, visible=False
        )

        def create_version_menu_items():
            items = []
            for version, data in reversed(list(versions_data.items())):
                def on_version_click(e):
                    state["selected_version"] = e.control.data
                    for item_container in versions_menu_column.controls:
                        is_selected = item_container.data == state["selected_version"]
                        item_container.border = ft.border.all(1, state["theme"]) if is_selected else None
                        item_container.bgcolor = ft.colors.with_opacity(0.2, state["theme"]) if is_selected else "transparent"
                    versions_menu.update()

                item_content = ft.Row([
                    ft.Icon(ft.icons.TERMINAL, size=18, color=state["theme"], tooltip=data["tooltip"]),
                    ft.Column([ft.Text(version, size=16), ft.Text(data["status"], color=data["color"], size=10) if data["status"] else ft.Container()], spacing=0)
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)

                is_selected_initial = version == state["selected_version"]
                items.append(
                    ft.Container(
                        content=item_content,
                        padding=ft.padding.symmetric(horizontal=15, vertical=5),
                        data=version,
                        on_click=on_version_click,
                        border_radius=5,
                        border=ft.border.all(1, state["theme"]) if is_selected_initial else None,
                        bgcolor=ft.colors.with_opacity(0.2, state["theme"]) if is_selected_initial else "transparent"
                    )
                )
            versions_menu_column.controls.clear()
            versions_menu_column.controls.extend(items)

        create_version_menu_items()
        
        version_button_icon = ft.Icon(ft.icons.KEYBOARD_ARROW_UP_SHARP, color=ft.colors.WHITE)
        def toggle_versions_menu(e):
            versions_menu.visible = not versions_menu.visible
            versions_menu.opacity = 1 if versions_menu.visible else 0
            version_button_icon.name = ft.icons.KEYBOARD_ARROW_DOWN_SHARP if versions_menu.visible else ft.icons.KEYBOARD_ARROW_UP_SHARP
            page.update()
            
        version_button = ft.Container(
            content=ft.Row([ft.Icon(ft.icons.REFRESH, color=ft.colors.WHITE), ft.Text("Выбрать версию", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE), version_button_icon], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=20, vertical=12), bgcolor=state["theme"], border_radius=30,
            on_click=toggle_versions_menu, tooltip="Выбрать версию игры", ink=True
        )
        
        def open_settings(e):
            page.window.width = 450
            page.window.height = 720
            page.window.center()
            switch_view(get_settings_view())

        async def on_settings_hover(e):
            icon_button = e.control.content
            icon_button.rotate = ft.Rotate(angle=pi * 2, alignment=ft.alignment.center) if e.data == "true" else ft.Rotate(angle=0)
            await icon_button.update_async()

        async def on_support_hover(e):
            icon_button = e.control.content
            icon_button.rotate = ft.Rotate(angle=0.25, alignment=ft.alignment.center) if e.data == "true" else ft.Rotate(angle=0)
            await icon_button.update_async()

        settings_and_support_row = ft.Row([
            ft.GestureDetector(content=ft.IconButton(icon=ft.icons.CONTACT_SUPPORT, icon_color=state["theme"], icon_size=35, tooltip="Задать вопрос", on_click=lambda _: page.launch_url("https://t.me/+M3_mdeOXMSE0MDky"), animate_rotation=ft.animation.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT)), on_hover=on_support_hover),
            ft.GestureDetector(content=ft.IconButton(icon=ft.icons.SETTINGS, icon_color=state["theme"], icon_size=35, tooltip="Настройки", on_click=open_settings, animate_rotation=ft.animation.Animation(duration=700, curve=ft.AnimationCurve.LINEAR)), on_hover=on_settings_hover),
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER)

        bottom_bar = ft.Container(
            content=ft.Stack([
                ft.Row([version_button], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([play_button], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([settings_and_support_row], alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ]),
            padding=ft.padding.symmetric(horizontal=20, vertical=15), height=80, bgcolor=ft.colors.with_opacity(0.2, ft.colors.BLACK),
            border=ft.border.only(top=ft.BorderSide(1, ft.colors.with_opacity(0.2, ft.colors.WHITE))),
        )
        
        view = ft.Column([main_area, bottom_bar], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True, spacing=0)
        return ft.Stack([view, versions_menu], expand=True)

    def get_settings_view():
        temp_state = state.copy()
        play_icon = ft.Icon(ft.icons.PLAY_ARROW, color=temp_state["theme"], size=24)
        
        def on_avatar_picked(e: ft.FilePickerResultEvent):
            if e.files:
                temp_state["avatar"] = e.files[0].path
                avatar_image.src = temp_state["avatar"]
                avatar_image.update()
        avatar_file_picker.on_result = on_avatar_picked
        
        def change_nick(e): temp_state["nick"] = e.control.value
        def on_auto_update_change(e): temp_state["auto_update"] = e.control.value
        
        auto_update_switch = ft.Switch(value=temp_state.get("auto_update", True), active_color=temp_state["theme"], on_change=on_auto_update_change)
        
        settings_container = ft.Container(
            content=ft.Column([
                ft.Row([play_icon, ft.Text("Лаунчер", weight=ft.FontWeight.BOLD, size=18)], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                ft.Divider(height=10, color=ft.colors.GREY_800, thickness=1), 
                ft.Row([ft.Text("Автообновления", size=18), auto_update_switch], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
            ], spacing=10),
            padding=15, border_radius=10, border=ft.border.all(2, temp_state["theme"]), bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_900), width=350
        )
        
        async def change_theme(e):
            e.control.scale = 1.2
            await e.control.update_async()
            choices = [c for c in dir(ft.colors) if c.isupper() and c not in ["WHITE", "BLACK", "TRANSPARENT"]]
            new_color_name = random.choice(choices)
            new_color = getattr(ft.colors, new_color_name)
            temp_state["theme"] = new_color
            
            nick_field.focused_border_color = new_color
            auto_update_switch.active_color = new_color
            palette_btn.icon_color = new_color
            play_icon.color = new_color
            settings_container.border = ft.border.all(2, new_color)
            save_button.style.bgcolor = new_color
            save_button.style.color = ft.colors.WHITE if new_color != ft.colors.WHITE else ft.colors.BLACK
            
            await asyncio.sleep(0.1)
            e.control.scale = 1
            await page.update_async()

        def save_and_exit(e):
            state.clear()
            state.update(temp_state)
            save_profile()
            page.window.width = 1000
            page.window.height = 720
            page.window.center()
            apply_theme()
            switch_view(get_main_view())
            
        avatar_image = ft.Image(src=temp_state["avatar"], width=90, height=90, fit=ft.ImageFit.COVER, border_radius=ft.border_radius.all(45))
        avatar_section = ft.Stack([
            avatar_image,
            ft.Container(content=ft.IconButton(icon=ft.icons.PHOTO_CAMERA, icon_size=20, icon_color=ft.colors.WHITE, on_click=lambda _: avatar_file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]), tooltip="Сменить аву"), right=0, bottom=0, bgcolor=ft.colors.with_opacity(0.7, ft.colors.BLACK), border_radius=ft.border_radius.all(30))
        ], width=90, height=90)
        
        nick_field = ft.TextField(value=temp_state["nick"], border_color="transparent", bgcolor=ft.colors.GREY_800, focused_border_color=temp_state["theme"], text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD), width=250, on_change=change_nick, border_radius=30, content_padding=ft.padding.symmetric(vertical=14, horizontal=20))
        
        palette_btn = ft.IconButton(icon=ft.icons.PALETTE, icon_size=60, icon_color=temp_state["theme"], tooltip="Сменить тему", on_click=change_theme, animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE))
        save_button = ft.ElevatedButton("Сохранить", width=350, on_click=save_and_exit, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=15, bgcolor=temp_state["theme"], color=ft.colors.WHITE if temp_state["theme"] != ft.colors.WHITE else ft.colors.BLACK, text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)))
        
        return center_col(
            ft.Row([avatar_section, nick_field], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            ft.Divider(height=10, color="transparent"),
            settings_container, palette_btn, save_button
        )

    def get_welcome_view():
        art1 = r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠉⠛⠿⣿⠅⠈⠀⠁⠀⢽⣿⣿⣿⠀⠁⠈⠀⠁⣿⡿⠛⠉
⠈⠀⠀⠀⠀⠀⢽⣿⣿⣿⠀⠀⠀⠀⠀⠁
⢽⣿⣿⣿
⢽⣿⣿⣿
⢽⣿⣿⣿
⣹⣿⣿⣿
⢺⣿⣿⣿
⠈⠙⠋⠁
"""
        view = center_col(
            ft.Text(art1, color=ft.colors.WHITE, font_family="Courier New", text_align=ft.TextAlign.CENTER),
            ft.Text("Прежде чем начать, давай познакомимся", color=ft.colors.WHITE, size=16),
            ft.ProgressBar(color=state["theme"], bgcolor="#444", bar_height=8, width=300, border_radius=5)
        )
        async def go_to_create():
            await asyncio.sleep(1) 
            switch_view(get_create_account_view())
        page.run_task(go_to_create)
        return view

    def get_create_account_view():
        nick_field = ft.TextField(hint_text="Как себя назовешь?", filled=True, bgcolor="#222", border_color="#555", color=ft.colors.WHITE, width=300, max_length=12, cursor_color="transparent", text_style=ft.TextStyle(weight=ft.FontWeight.BOLD))
        avatar_display_container = ft.Container(width=90, height=90, alignment=ft.alignment.center, border_radius=ft.border_radius.all(45), clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=ft.Icon(ft.icons.ACCOUNT_CIRCLE_SHARP, size=80, color=state["theme"]))
        
        def on_avatar_picked(e: ft.FilePickerResultEvent):
            if e.files:
                state["avatar"] = e.files[0].path
                avatar_display_container.content = ft.Image(src=state["avatar"], width=90, height=90, fit=ft.ImageFit.COVER)
                page.update()
        avatar_file_picker.on_result = on_avatar_picked
        
        select_avatar_button = ft.IconButton(icon=ft.icons.ADD_A_PHOTO, icon_size=30, icon_color=ft.colors.WHITE, tooltip="Выбрать аву", on_click=lambda _: avatar_file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]))
        avatar_section = ft.Column([avatar_display_container, select_avatar_button], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
        
        def create_account(e):
            if not nick_field.value or not state.get("avatar"):
                page.open(ft.SnackBar(ft.Text("Пожалуйста, введи ник и выбери аву.", color=ft.colors.WHITE), bgcolor=ft.colors.RED_ACCENT_700, duration=1500))
                return
            state["nick"] = nick_field.value
            switch_view(get_theme_view())
            
        continue_button = ft.ElevatedButton(content=ft.Text("Продолжить", weight=ft.FontWeight.BOLD), style=ft.ButtonStyle(bgcolor=ft.colors.WHITE, color=ft.colors.BLACK, shape=ft.RoundedRectangleBorder(radius=10)), on_click=create_account)
        progress = ft.ProgressBar(value=0.25, color=state["theme"], bgcolor="#444", bar_height=8, width=300, border_radius=5)
        return center_col(avatar_section, ft.Text("Создай аккаунт", color=ft.colors.WHITE, size=20), nick_field, progress, continue_button)

    def get_theme_view():
        title = ft.Text("Выбери тему лаунчера - просто кликни на палитру", color=ft.colors.WHITE, size=20, text_align=ft.TextAlign.CENTER, width=350)
        progress = ft.ProgressBar(value=0.5, color=state["theme"], bgcolor="#444", bar_height=8, width=300, border_radius=5)
        
        def save_theme_and_next():
            apply_theme()
            switch_view(get_support_view())
            
        continue_btn = ft.ElevatedButton(content=ft.Text("Продолжить", weight=ft.FontWeight.BOLD), style=ft.ButtonStyle(bgcolor=state["theme"], color=ft.colors.WHITE if state["theme"] != ft.colors.WHITE else ft.colors.BLACK, shape=ft.RoundedRectangleBorder(radius=10)), on_click=lambda _: save_theme_and_next())
        
        async def select_random_theme(e):
            e.control.scale = 1.2
            await e.control.update_async()
            choices = [c for c in dir(ft.colors) if c.isupper() and c not in ["WHITE", "BLACK", "TRANSPARENT"]]
            new_color = getattr(ft.colors, random.choice(choices))
            state["theme"] = new_color
            palette_btn.icon_color = new_color
            title.color = new_color
            progress.color = new_color 
            continue_btn.style.bgcolor = new_color
            continue_btn.style.color = ft.colors.WHITE if new_color != ft.colors.WHITE else ft.colors.BLACK
            await asyncio.sleep(0.1)
            e.control.scale = 1
            await page.update_async()
            
        palette_btn = ft.IconButton(icon=ft.icons.PALETTE, icon_size=80, icon_color=state["theme"], tooltip="Сменить цвет", on_click=select_random_theme, animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE))
        return center_col(title, palette_btn, progress, continue_btn)

    def get_support_view():
        dashed_rect = ft.canvas.Rect(0, 0, 298, 148, border_radius=15, paint=ft.Paint(stroke_width=2, color=ft.colors.GREY_700, stroke_dash_pattern=[6, 4], style=ft.PaintingStyle.STROKE))
        drop_content = ft.Column([ft.Icon(ft.icons.IMAGE, size=50, color=ft.colors.GREY_400), ft.Text("Сюда кидай скрин подписки", color=ft.colors.GREY_400)], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        screenshot_drop_area = ft.Container(
            content=ft.Stack([
                ft.canvas.Canvas([dashed_rect], width=300, height=150),
                ft.Container(content=drop_content, width=300, height=150, alignment=ft.alignment.center, border_radius=ft.border_radius.all(15), on_click=lambda _: screenshot_file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]) if not screenshot_drop_area.disabled else None)
            ]),
            disabled=True, opacity=0.5
        )
        continue_button_support = ft.ElevatedButton(content=ft.Text("Продолжить", weight=ft.FontWeight.BOLD), width=250, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=lambda _: page.run_task(start_final_step_countdown), disabled=True, opacity=0.5)
        
        def on_screenshot_picked(e: ft.FilePickerResultEvent):
            if e.files:
                drop_content.controls.clear()
                drop_content.controls.append(ft.Icon(ft.icons.CHECK_CIRCLE, size=70, color=state["theme"]))
                continue_button_support.disabled = False
                continue_button_support.opacity = 1
                continue_button_support.style.bgcolor = state["theme"]
                continue_button_support.style.color = ft.colors.WHITE if state["theme"] != ft.colors.WHITE else ft.colors.BLACK
                page.update()
        screenshot_file_picker.on_result = on_screenshot_picked
        
        def handle_subscribe_click(e):
            screenshot_drop_area.disabled = False
            screenshot_drop_area.opacity = 1.0
            dashed_rect.paint.color = state["theme"]
            page.update()
            
        subscribe_button = ft.ElevatedButton(width=250, content=ft.Row([ft.Text("Подписаться", weight=ft.FontWeight.BOLD), ft.Icon(ft.icons.TELEGRAM)], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=10), url="https://t.me/addlist/l4SKruXSbc5mZmQ6", url_target="_blank", on_click=handle_subscribe_click, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=state["theme"], color=ft.colors.WHITE if state["theme"] != ft.colors.WHITE else ft.colors.BLACK))
        progress = ft.ProgressBar(value=0.75, color=state["theme"], bgcolor="#444", bar_height=8, width=300, border_radius=5)
        view = center_col(
            ft.Row([ft.Icon(ft.icons.TAG_FACES_OUTLINED, color=ft.colors.WHITE), ft.Text("Поддержи разработчика", color=ft.colors.WHITE, size=20)], alignment=ft.MainAxisAlignment.CENTER),
            progress, screenshot_drop_area, subscribe_button, continue_button_support
        )
        return view

    def get_final_view():
        avatar_ctrl = ft.Container(width=120, height=120, content=ft.Image(src=state["avatar"], width=120, height=120, fit=ft.ImageFit.COVER), clip_behavior=ft.ClipBehavior.ANTI_ALIAS, border_radius=ft.border_radius.all(60))
        progress = ft.ProgressBar(value=1.0, color=state["theme"], bgcolor="#444", bar_height=8, width=300, border_radius=5, animate_size=300)
        view = center_col(avatar_ctrl, ft.Text(f"Рад знакомству, {state['nick']}", color=ft.colors.WHITE, size=24, weight=ft.FontWeight.BOLD), progress)
        return view

    page.add(main_content)
    apply_theme()
    page.run_task(run_startup_sequence)

if __name__ == "__main__":
    if "--run-totem" in sys.argv:
        exit_code = totem.main()
        sys.exit(exit_code)

    ft.app(target=main)
