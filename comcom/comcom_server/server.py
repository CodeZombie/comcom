from typing import List, Dict
from nicegui import ui
from comcom.comcom import ComCom, Recipe
from comcom.comfy_ui.file_management.media_metadata import MediaMetadata
import random
import logging
import asyncio
from PIL import Image
import base64
from io import BytesIO

# You can't stick a recipe in a UI element, so if we do use Trees, we have to give them UUIDs for IDs and map that UUID to the full path to the recipe
# and execute the recipe from that full path :-)

class ComComServer:
    def __init__(self):
        ui.page_title("ComCom")
        self.comcom = ComCom()
        self.selected_recipe_file: str = ""
        self.selected_recipes: List[Recipe] = []

        self.is_executing = False


        # ui.add_head_html('<style>.q-drawer--left { width: 20% !important }</style>')
        # ui.add_head_html('<style>.q-drawer--right { width: 20% !important }</style>')

        with ui.header().classes('items-center justify-between'):
            ui.label('ComCom Recipe Executor').classes('text-xl')
            ui.space()
            self.progress_bar = ui.linear_progress(color='warning').classes('w-1/4')
            ui.button("Halt").props('color=red').on_click(self.interrupt).bind_enabled_from(self, 'is_executing')
            ui.button("Refresh").on_click(self.refresh)

        with ui.left_drawer():
            with ui.row().classes('w-full'):
                self.recipe_file_selector()
            
            with ui.row().classes('w-full'):
                self.log = ui.code(language='markdown').style('white-space: pre-wrap').classes('w-full break-all')
                self.log.bind_visibility(self.log, 'content')

            with ui.row().classes('w-full'):
                self.recipe_tree()

        #with ui.element('div').classes('w-full h-screen flex items-center justify-center p-0'):
        with ui.tabs().classes('w-full h-full') as tabs:
            latent_preview_tab = ui.tab('Preview')
            finished_images_tab = ui.tab('Generated Images')
        with ui.tab_panels(tabs, value=latent_preview_tab).classes('w-full h-full').style('background: 0;'):
                with ui.tab_panel(latent_preview_tab).classes('w-full items-center justify-center'):
                    IMAGE_URL = "https://i.pinimg.com/736x/95/47/0c/95470c8d65cb8bc6801814bbdf76f98b.jpg"
                    self.preview_image = ui.image(IMAGE_URL).classes('w-[500px] h-auto max-w-full max-h-full shadow-xl')
                with ui.tab_panel(finished_images_tab).classes('w-full items-center justify-center'):
                    IMAGE_URL = "https://fastly.picsum.photos/id/684/640/360.jpg?hmac=XI9EvJ5cgD5EOo18eNf8BT62dp9CIb42ifOw1G5D-R0"
                    with ui.row():
                        self.final_image = ui.image(IMAGE_URL).classes('w-[500px] h-auto max-w-full max-h-full shadow-xl')
                    with ui.row():
                        self.final_image_table = ui.table(columns=[
                            {'name': 'property', 'label': "Property", 'field': 'property', 'align': 'left'},
                            {'name': 'value', 'label': 'Value', 'field': 'value', 'align': 'right'}
                            ],
                            rows=[],
                            ).classes('w-full')
                    with ui.row():
                        ui.space()
                        self.thumbnail_row()
                

        with ui.right_drawer():
            self.recipe_details()

        ui.run(dark=True)

    def refresh(self):
        self.comcom = ComCom()
        selected_recipe_global_ids = [r.global_id for r in self.selected_recipes]
        self.select_recipe_file(self.selected_recipe_file)
        self.select_recipes(selected_recipe_global_ids)
        self.recipe_file_selector.refresh()
        self.recipe_tree.refresh()
        self.recipe_details.refresh()


    def select_recipe_file(self, file_name: str) -> None:
        self.log.content = ''
        try:
            self.comcom.select_recipe_file(file_name)
            self.selected_recipe_file = file_name
        except Exception as e:
            self.log.content = str(e)

        self.recipe_tree.refresh()

    def select_recipes(self, recipe_global_ids: List[str]) -> None:
        self.selected_recipes = []
        for global_id in recipe_global_ids:
            self.selected_recipes.append(self.comcom.get_recipe(global_id))
        self.recipe_details.refresh()
        self.thumbnail_row.refresh()

    @ui.refreshable
    def thumbnail_row(self):
        def set_primary_generated_image(name: str, media_metadata: MediaMetadata | str):
            self.final_image_table.rows = []

            if isinstance(media_metadata, str):
                self.final_image.source = media_metadata
            else:
                self.final_image.source = media_metadata.local_path.path_str
                new_rows = [
                    {'property': 'name', 'value': media_metadata.local_path.name},
                    {'property': 'stored sha1', 'value': media_metadata.sha1},
                    {'property': 'file sha1', 'value': media_metadata.local_path.sha1},
                    {'property': 'requires editing', 'value': media_metadata.local_path.requires_editing},
                ]
                if media_metadata.local_path.requires_editing:
                    new_rows.append({'property': 'has been edited', 'value': media_metadata.local_file_needs_to_be_edited_but_hasnt_been_edited_yet})
                self.final_image_table.add_rows(new_rows)
                self.final_image_table.update()

        all_media_metadata = {}
        for recipe in self.selected_recipes:
            for name, meta in recipe.saved_media_metadata.items():
                if not meta:
                    continue
                all_media_metadata[f"{recipe.global_id}.{name}"] = meta

        with ui.row().classes('flex-nowrap overflow-x-auto gap-4 p-2'):
            for key, value in all_media_metadata.items():
                ui.image(value.local_path.path_str).classes('w-24 h-24 object-cover rounded-md shadow-md cursor-pointer transition-transform hover:scale-105') \
                    .on('click', lambda key=key, value=value: set_primary_generated_image(key, value))
                
        if len(all_media_metadata) > 0:
            set_primary_generated_image(list(all_media_metadata.keys())[0], list(all_media_metadata.values())[0])
        else:
            set_primary_generated_image("None", "https://cdn-icons-png.flaticon.com/512/5978/5978100.png")

    # def media_metadata(self, media_metadata: MediaMetadata):
    #     # saved_media_metadata
    #     with ui.column().classes('w-full'):
    #         with ui.row().classes('w-full'):
    #             ui.image(img_data).classes('w-24 h-24 object-cover rounded-md shadow-md cursor-pointer transition-transform hover:scale-105') \
    #                 .on('click', lambda data=img_data: set_primary_generated_image(data))

    @classmethod
    def recipe_to_ui_list(cls, recipe: Recipe):
        if not recipe:
            return []
        
        new_ui_element = {
            'id': recipe.global_id,
            'label': str(recipe.id), 
            'children': []
        }
        for r in recipe.recipes.values():
            new_ui_element['children'].extend(cls.recipe_to_ui_list(r))

        return [new_ui_element]
    
    @ui.refreshable
    def recipe_file_selector(self):
        file_options = {file: file for file in self.comcom.recipe_files}
        s = ui.select(
            options=file_options, 
            value=self.selected_recipe_file or None,
            label='Recipe File', 
            on_change=lambda e: self.select_recipe_file(e.value)
        ).classes('w-full')
    
    @ui.refreshable
    def recipe_tree(self):
        t = ui.tree(
            ComComServer.recipe_to_ui_list(self.comcom.selected_recipe), 
            tick_strategy='strict') \
            .expand() \
            .on_tick(lambda e: self.select_recipes(e.value))
        t.tick([r.global_id for r in self.selected_recipes])
        
    @ui.refreshable
    def recipe_details(self):
        for selected_recipe in self.selected_recipes:
            with ui.card().classes('w-full'):
                ui.label(selected_recipe.id)
                ui.label(selected_recipe.workflow)
                for node_name, params in (selected_recipe.nodes | selected_recipe.load | selected_recipe.save).items():
                    if isinstance(params, dict):
                        with ui.expansion(node_name).classes('w-full'):
                            for param_name, param_value in params.items():
                                self.create_element_from_param(param_name, param_value)
                    else:
                        self.create_element_from_param(node_name, params)

                with ui.row().classes('w-full'):
                    ui.space()
                    ui.button("Execute", on_click=lambda: self.execute_recipe(selected_recipe)) \
                    .bind_enabled_from(self, 'is_executing', backward=lambda v: not v)

    def create_element_from_param(self, param_name, param_value) -> None:
        if isinstance(param_value, str):
            ui.textarea(param_name, value=param_value).classes('w-full').props('autogrow').disable()
        if isinstance(param_value, int):
            ui.number(param_name, value=param_value).classes('w-full').disable()
        if isinstance(param_value, float):
            ui.number(param_name, value=param_value, precision=3).classes('w-full').disable()
        if isinstance(param_value, list):
            ui.textarea(param_name, value='\n'.join(param_value)).classes('w-full').props('autogrow').disable()
        if isinstance(param_value, dict):
            for k, v in param_value.items():
                self.create_element_from_param(f"{param_name}.{k}", v)

    async def execute_recipe(self, recipe) -> int:
        self.is_executing = True
        await asyncio.to_thread(self.comcom.execute_recipe, recipe, self.on_execute_progress, self.on_preview_image)
        self.is_executing = False
        self.thumbnail_row.refresh()
        self.progress_bar.value = 0



    def interrupt(self):
        self.comcom.interrupt()
        self.progress_bar.value = 0
        self.is_executing = False

    def on_preview_image(self, image: Image):
        self.preview_image.set_source(self.pil_image_to_base64(image))

    def pil_image_to_base64(self, pil_image: Image):
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        buffered.seek(0)
        base64_encoded_bytes = base64.b64encode(buffered.read())
        return 'data:image/png;base64,' + base64_encoded_bytes.decode('ascii')

    def on_execute_progress(self, *args, **kwargs):
        self.progress_bar.value = args[1] / args[2]
