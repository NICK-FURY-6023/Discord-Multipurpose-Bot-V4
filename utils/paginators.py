from __future__ import annotations

import discord
from discord.ext import menus
from discord.ext import commands
from .paginator import Paginator as HackerPaginator
from discord.ext.commands import Context, Paginator as CmdPaginator
from typing import Any

from utils.config import *


class FieldPagePaginator(menus.ListPageSource):

    def __init__(self,
                 entries: list[tuple[Any, Any]],
                 *,
                 per_page: int = 10,
                 inline: bool = False,
                 **kwargs) -> None:
        super().__init__(entries, per_page=per_page)
        self.embed: discord.Embed = discord.Embed(
            title=kwargs.get('title'),
            description=kwargs.get('description'),
            color=0x01f5b6)
        self.inline: bool = inline

    async def format_page(self, menu: HackerPaginator,
                          entries: list[tuple[Any, Any]]) -> discord.Embed:
        self.embed.clear_fields()

        for key, value in entries:
            self.embed.add_field(name=key, value=f"{value}\n\n", inline=self.inline)

        maximum = self.get_max_pages()
        if maximum > 1:
            text = f'{NAME} • Page {menu.current_page + 1}/{maximum}'
            self.embed.set_footer(
                text=text,
                icon_url=
                "https://images-ext-1.discordapp.net/external/CdPZdE5M2e2FgJwM7Lein19vYLahi27f_lAbjVoRczI/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1071821844006576159/a_26eeac3b80c943b4142976461acf2034.gif?width=115&height=115"
            )
            self.embed.timestamp = discord.utils.utcnow()
        return self.embed


class TextPaginator(menus.ListPageSource):

    def __init__(self, text, *, prefix='```', suffix='```', max_size=2000):
        pages = CmdPaginator(prefix=prefix,
                             suffix=suffix,
                             max_size=max_size - 200)
        for line in text.split('\n'):
            pages.add_line(line)

        super().__init__(entries=pages.pages, per_page=1)

    async def format_page(self, menu, content):
        maximum = self.get_max_pages()
        if maximum > 1:
            return f'{content}\n{NAME} • Page {menu.current_page + 1}/{maximum}'
        return content


class DescriptionEmbedPaginator(menus.ListPageSource):

    def __init__(self,
                 entries: list[Any],
                 *,
                 per_page: int = 10,
                 **kwargs) -> None:
        super().__init__(entries, per_page=per_page)
        self.embed: discord.Embed = discord.Embed(
            title=kwargs.get('title'),
            color=0x01f5b6,
        )

    async def format_page(self, menu: HackerPaginator,
                          entries: list[tuple[Any, Any]]) -> discord.Embed:
        self.embed.clear_fields()

        self.embed.description = '\n'.join(entries)
        self.embed.timestamp = discord.utils.utcnow()
        maximum = self.get_max_pages()
        if maximum > 1:
            text = f'Anxious • Page {menu.current_page + 1}/{maximum}'
            self.embed.set_footer(
                text=text,
                icon_url=
                "https://images-ext-1.discordapp.net/external/CdPZdE5M2e2FgJwM7Lein19vYLahi27f_lAbjVoRczI/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1071821844006576159/a_26eeac3b80c943b4142976461acf2034.gif?width=115&height=115"
            )

        return self.embed
