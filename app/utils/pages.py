from typing import List, Callable, Any

from discord.ext.pages import Page, Paginator

from pydantic import BaseModel


def group_items(
    items: List[Any],
    group_by: int,
):
    return [items[i:i+group_by] for i in range(0, len(items), group_by)]


async def gather_pages(
    construct_embed: Callable,
    element_groups: List[List[BaseModel]],
) -> Paginator:
    pages = list()
    for element_group in element_groups:
        pages.append(
            Page(
                embeds=[
                    await construct_embed(element)
                    for element
                    in element_group
                ]
            )
        )
    return Paginator(pages=pages)
