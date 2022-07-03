from textual.app import App
from textual import events
from textual.views import GridView
from textual.reactive import Reactive
from textual.layouts.dock import DockLayout
from textual.widget import Widget
from textual.widgets import Header, Footer, Placeholder

class ConsoleInterface(Widget):
    display = Reactive("0") 

    async def on_mount(self, event: events.Mount) -> None:
        pass

class MainInterface(App):

    async def on_mount(self):
        # await self.view.dock(ConsoleInterface())
            
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(Placeholder(), edge="left", size=30, name="sidebar")
        await self.view.dock(Placeholder(), edge="left", size=30, name="rightbar")

    async def on_load(self):
        await self.bind("q", "quit")

    async def on_key(self, event: events.Key) -> None:
        print(event)
        # self.console.print(event)


MainInterface.run()