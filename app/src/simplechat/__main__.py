"""
simplechat - chat with AI
    Copyright (C) 2024 Michael Manis - michaelmanis@tutanota.com
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys

import uvicorn

# Leave this import in to explicitly "link" simplechat:app
#   to this file in the import tree. Just in case
from simplechat import app
from simplechat.settings import settings


def main():
    uvicorn.run(
        "simplechat:app",
        host=settings().host,
        port=settings().port,
        reload=settings().hot_reload,
    )


if __name__ == "__main__":
    main()
    sys.exit(0)
