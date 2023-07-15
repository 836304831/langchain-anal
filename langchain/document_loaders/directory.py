"""Load documents from a directory."""
import concurrent
import logging
from pathlib import Path
from typing import Any, List, Optional, Type, Union

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.html_bs import BSHTMLLoader
from langchain.document_loaders.text import TextLoader
from langchain.document_loaders.unstructured import UnstructuredFileLoader

FILE_LOADER_TYPE = Union[
    Type[UnstructuredFileLoader], Type[TextLoader], Type[BSHTMLLoader]
]
logger = logging.getLogger(__name__)


def _is_visible(p: Path) -> bool:
    parts = p.parts
    for _p in parts:
        if _p.startswith("."):
            return False
    return True


class DirectoryLoader(BaseLoader):
    """Load documents from a directory."""

    def __init__(
        self,
        path: str,
        glob: str = "**/[!.]*",
        silent_errors: bool = False,
        load_hidden: bool = False,
        loader_cls: FILE_LOADER_TYPE = UnstructuredFileLoader,
        loader_kwargs: Union[dict, None] = None,
        recursive: bool = False,
        show_progress: bool = False,
        use_multithreading: bool = False,
        max_concurrency: int = 4,
    ):
        """Initialize with a path to directory and how to glob over it.

        Args:
            path: Path to directory.
            glob: Glob pattern to use to find files. Defaults to "**/[!.]*"
               (all files except hidden).
            silent_errors: Whether to silently ignore errors. Defaults to False.
            load_hidden: Whether to load hidden files. Defaults to False.
            loader_cls: Loader class to use for loading files.
              Defaults to UnstructuredFileLoader.
            loader_kwargs: Keyword arguments to pass to loader_cls. Defaults to None.
            recursive: Whether to recursively search for files. Defaults to False.
            show_progress: Whether to show a progress bar. Defaults to False.
            use_multithreading: Whether to use multithreading. Defaults to False.
            max_concurrency: The maximum number of threads to use. Defaults to 4.
        """
        if loader_kwargs is None:
            loader_kwargs = {}
        self.path = path
        self.glob = glob
        self.load_hidden = load_hidden
        self.loader_cls = loader_cls
        self.loader_kwargs = loader_kwargs
        self.silent_errors = silent_errors
        self.recursive = recursive
        self.show_progress = show_progress
        self.use_multithreading = use_multithreading
        self.max_concurrency = max_concurrency

    def load_file(
        self, item: Path, path: Path, docs: List[Document], pbar: Optional[Any]
    ) -> None:
        """Load a file.

        Args:
            item: File path.
            path: Directory path.
            docs: List of documents to append to.
            pbar: Progress bar. Defaults to None.
        """
        if item.is_file():
            if _is_visible(item.relative_to(path)) or self.load_hidden:
                try:
                    sub_docs = self.loader_cls(str(item), **self.loader_kwargs).load()
                    docs.extend(sub_docs)
                except Exception as e:
                    if self.silent_errors:
                        logger.warning(e)
                    else:
                        raise e
                finally:
                    if pbar:
                        pbar.update(1)

    def load(self) -> List[Document]:
        """Load documents."""
        p = Path(self.path)
        if not p.exists():
            raise FileNotFoundError(f"Directory not found: '{self.path}'")
        if not p.is_dir():
            raise ValueError(f"Expected directory, got file: '{self.path}'")

        docs: List[Document] = []
        items = list(p.rglob(self.glob) if self.recursive else p.glob(self.glob))

        pbar = None
        if self.show_progress:
            try:
                from tqdm import tqdm

                pbar = tqdm(total=len(items))
            except ImportError as e:
                logger.warning(
                    "To log the progress of DirectoryLoader you need to install tqdm, "
                    "`pip install tqdm`"
                )
                if self.silent_errors:
                    logger.warning(e)
                else:
                    raise e

        if self.use_multithreading:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.max_concurrency
            ) as executor:
                executor.map(lambda i: self.load_file(i, p, docs, pbar), items)
        else:
            for i in items:
                self.load_file(i, p, docs, pbar)

        if pbar:
            pbar.close()

        return docs


#
