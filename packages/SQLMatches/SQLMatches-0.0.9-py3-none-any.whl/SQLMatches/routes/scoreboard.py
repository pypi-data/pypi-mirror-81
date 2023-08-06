# -*- coding: utf-8 -*-

"""
GNU General Public License v3.0 (GPL v3)
Copyright (c) 2020-2020 WardPearce
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse
from ..templating import TEMPLATE

from ..community import Community
from ..community.exceptions import InvalidMatchID


class ScoreboardPage(HTTPEndpoint):
    async def get(self, request):
        try:
            scoreboard = await Community(
                request.path_params["community"]
            ).match(request.path_params["match_id"]).scoreboard()
        except InvalidMatchID:
            return RedirectResponse(
                request.url_for(
                    "CommunityPage",
                    community=request.path_params["community"]
                )
            )
        else:
            return TEMPLATE.TemplateResponse(
                "scoreboard.html", {
                    "request": request,
                    "scoreboard": scoreboard
                })
