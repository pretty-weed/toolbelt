from types import CapsuleType
from typing import Any, Callable, Self, SupportsIndex, override
from warnings import deprecated

# =======
# ints
# =======

BUTTON_ABORT: int
BUTTON_CANCEL: int
BUTTON_DEFAULT: int
BUTTON_ESCAPE: int
BUTTON_IGNORE: int
BUTTON_NO: int
BUTTON_OK: int
BUTTON_RETRY: int
BUTTON_YES: int

CAP_ROUND: int
CSPACE_UNDEFINED: int

ITEMTYPE_ARC: int
ITEMTYPE_GROUP: int
ITEMTYPE_LATEXFRAME: int
ITEMTYPE_MULTIPLE: int
ITEMTYPE_NOTEFRAME: int
ITEMTYPE_OSGFRAME: int
ITEMTYPE_PATHTEXT: int
ITEMTYPE_POLYGON: int
ITEMTYPE_SYMBOL: int
ITEMTYPE_TABLE: int

NOFACINGPAGES: int
FACINGPAGES: int
FIRSTPAGELEFT: int
FIRSTPAGERIGHT: int

PAGE_1: int
PAGE_2: int
PAGE_3: int
PAGE_4: int

PORTRAIT: int
LANDSCAPE: int

JOIN_BEVEL: int
JOIN_ROUND: int
LUMINOSITY: int
SATURATION: int
SOFT_LIGHT: int
UNIT_CICERO: int
UNIT_CM: int
UNIT_INCHES: int
UNIT_MM: int
UNIT_PICAS: int
UNIT_PT: int
# =======
# types
# =======

class ImageExport:
    def __init__(self) -> None: ...
    @override
    def __delattr__(self, name: str) -> None: ...
    @override
    def __dir__(self) -> list[str]: ...
    __doc__: str
    @override
    def __eq__(self, value: Any) -> bool: ...
    @override
    def __format__(self, format_spec: str): ...
    def __ge__(self, value: Any) -> bool: ...
    @override
    def __getattribute__(self, name: str) -> Any: ...
    @override
    def __getstate__(self) -> dict[str, Any]: ...
    def __gt__(self, value: Any) -> bool: ...
    @override
    def __hash__(self) -> int: ...
    def __init_subclass__(cls) -> None: ...
    def __le__(self, value: Any) -> bool: ...
    def __lt__(self, value: Any) -> bool: ...
    @override
    def __ne__(self, value: Any) -> bool: ...
    # ToDo Figure out what `Any`s should be
    def __new__(cls, *args: Any, **kwargs: Any) -> Self: ...
    @override
    def __reduce__(self) -> tuple[Any, ...]: ...
    @override
    def __reduce_ex__(
        self, protocol: SupportsIndex
    ) -> tuple[Any, ...]: ...  # TODO this could be more explicit return
    @override
    def __setattr__(self, name: str, value: Any) -> None: ...
    @override
    def __sizeof__(self) -> int: ...
    allTypes: list[str]
    dpi: int
    name: str
    quality: int
    def save(self) -> bool: ...
    def saveAs(self) -> bool: ...
    scale: int
    transparentBkgnd: int
    type: str

class NameExistsError(Exception): ...
class NoDocOpenError(Exception): ...
class NoValidObjectError(Exception): ...
class NotFoundError(Exception): ...

class PDFfile:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    __doc__: str
    def __gt__(self: Self, value: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __init_subclass__(cls) -> None: ...
    aanot: int
    achange: int
    acopy: int
    allowAnnots: int
    allowChange: int
    allowCopy: int
    allowPrinting: int
    aprint: int
    article: int
    binding: int
    bleedMarks: int
    # bleedb: <class 'member_descriptor'>
    # bleedl: <class 'member_descriptor'>
    # bleedr: <class 'member_descriptor'>
    # bleedt: <class 'member_descriptor'>
    # bookmarks: <class 'member_descriptor'>
    # colorMarks: <class 'member_descriptor'>
    # compress: <class 'member_descriptor'>
    # compressmtd: <class 'member_descriptor'>
    # cropMarks: <class 'member_descriptor'>
    # displayBookmarks: <class 'member_descriptor'>
    # displayFullscreen: <class 'member_descriptor'>
    # displayLayers: <class 'member_descriptor'>
    # displayThumbs: <class 'member_descriptor'>
    # doClip: <class 'member_descriptor'>
    # docInfoMarks: <class 'member_descriptor'>
    # domulti: <class 'member_descriptor'>
    # downsample: <class 'getset_descriptor'>
    # effval: <class 'getset_descriptor'>
    # embedPDF: <class 'member_descriptor'>
    # encrypt: <class 'member_descriptor'>
    file: str
    # fitWindow: <class 'member_descriptor'>
    # fontEmbedding: <class 'getset_descriptor'>
    # fonts: <class 'getset_descriptor'>
    # hideMenuBar: <class 'member_descriptor'>
    # hideToolBar: <class 'member_descriptor'>
    # imagepr: <class 'getset_descriptor'>
    # info: <class 'getset_descriptor'>
    # intenti: <class 'member_descriptor'>
    # intents: <class 'member_descriptor'>
    # isGrayscale: <class 'member_descriptor'>
    # lpival: <class 'getset_descriptor'>
    # markLength: <class 'member_descriptor'>
    # markOffset: <class 'member_descriptor'>
    # mirrorH: <class 'member_descriptor'>
    # mirrorV: <class 'member_descriptor'>
    # noembicc: <class 'member_descriptor'>
    # openAction: <class 'getset_descriptor'>
    # outdst: <class 'member_descriptor'>
    # owner: <class 'getset_descriptor'>
    # pageLayout: <class 'member_descriptor'>
    # pages: <class 'getset_descriptor'>
    # presentation: <class 'member_descriptor'>
    # printprofc: <class 'getset_descriptor'>
    # profilei: <class 'member_descriptor'>
    # profiles: <class 'member_descriptor'>
    # quality: <class 'member_descriptor'>
    # registrationMarks: <class 'member_descriptor'>
    # resolution: <class 'getset_descriptor'>
    # rotateDeg: <class 'getset_descriptor'>
    def save(self) -> None: ...
    # solidpr: <class 'getset_descriptor'>
    # subsetList: <class 'getset_descriptor'>
    # thumbnails: <class 'member_descriptor'>
    # useDocBleeds: <class 'member_descriptor'>
    # useLayers: <class 'member_descriptor'>
    # uselpi: <class 'member_descriptor'>
    # user: <class 'getset_descriptor'>
    # usespot: <class 'member_descriptor'>
    # version: <class 'member_descriptor'>

class Printer:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __dir__(self) -> list[str]: ...
    __doc__: str
    def __eq__(self: Self, value: Any) -> bool: ...
    def __format__(self, format_spec): ...
    def __ge__(self: Self, value: Any) -> bool: ...
    def __getattribute__(self, name: str) -> Any: ...
    @override
    def __getstate__(self) -> dict[str, Any]: ...
    def __gt__(self: Self, value: Any) -> bool: ...
    def __hash__(self): ...
    def __init_subclass__(cls) -> None: ...
    def __le__(self: Self, value: Any) -> bool: ...
    def __lt__(self: Self, value: Any) -> bool: ...
    @override
    def __ne__(self: Self, value: Any) -> bool: ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Self: ...
    @override
    def __reduce__(self) -> tuple[Any, ...]: ...
    def __reduce_ex__(
        self, protocol: SupportsIndex
    ) -> tuple[Any, ...]: ...  # TODO this could be more explicit return
    def __setattr__(self, name, value): ...
    def __sizeof__(self): ...
    # allPrinters: <class 'getset_descriptor'>
    # cmd: <class 'getset_descriptor'>
    # color: <class 'member_descriptor'>
    # copies: <class 'member_descriptor'>
    # file: <class 'getset_descriptor'>
    # mph: <class 'member_descriptor'>
    # mpv: <class 'member_descriptor'>
    # pages: <class 'getset_descriptor'>
    def printNow(self): ...
    # printer: <class 'getset_descriptor'>
    # prnLanguage: <class 'member_descriptor'>
    # pslevel: <class 'member_descriptor'>
    # separation: <class 'getset_descriptor'>
    # ucr: <class 'member_descriptor'>
    # useICC: <class 'member_descriptor'>

class ScribusException(Exception): ...
class WrongFrameTypeError(Exception): ...

# =======
# tuples
# =======

PAPER_A0: tuple[float, float]
PAPER_A0_MM: tuple[float, float]
PAPER_A1: tuple[float, float]
PAPER_A1_MM: tuple[float, float]
PAPER_A2: tuple[float, float]
PAPER_A2_MM: tuple[float, float]
PAPER_A3: tuple[float, float]
PAPER_A3_MM: tuple[float, float]
PAPER_A4: tuple[float, float]
PAPER_A7: tuple[float, float]
PAPER_A5: tuple[float, float]
PAPER_A8: tuple[float, float]
PAPER_A6: tuple[float, float]
PAPER_A9: tuple[float, float]
PAPER_A7_MM: tuple[float, float]
PAPER_A8_MM: tuple[float, float]
PAPER_A9_MM: tuple[float, float]
PAPER_B0: tuple[float, float]
PAPER_B0_MM: tuple[float, float]
PAPER_B1: tuple[float, float]
PAPER_B10: tuple[float, float]
PAPER_B10_MM: tuple[float, float]
PAPER_B1_MM: tuple[float, float]
PAPER_B2: tuple[float, float]
PAPER_B2_MM: tuple[float, float]
PAPER_B3: tuple[float, float]
PAPER_B3_MM: tuple[float, float]
PAPER_B4: tuple[float, float]
PAPER_B4_MM: tuple[float, float]
PAPER_B5: tuple[float, float]
PAPER_B5_MM: tuple[float, float]
PAPER_B6: tuple[float, float]
PAPER_B6_MM: tuple[float, float]
PAPER_B7: tuple[float, float]
PAPER_B7_MM: tuple[float, float]
PAPER_B8: tuple[float, float]
PAPER_B8_MM: tuple[float, float]
PAPER_B9: tuple[float, float]
PAPER_B9_MM: tuple[float, float]
PAPER_C5E: tuple[float, float]
PAPER_COMM10E: tuple[float, float]
PAPER_DLE: tuple[float, float]
PAPER_EXECUTIVE: tuple[float, float]
PAPER_FOLIO: tuple[float, float]
PAPER_LEDGER: tuple[float, float]
PAPER_LEGAL: tuple[float, float]
PAPER_LETTER: tuple[float, float]
PAPER_TABLOID: tuple[float, float]
SCRIBUS_VERSION_INFO: tuple[int, int, int, str, int]
# =======
# <class 'str'>s
# =======

SCRIBUS_VERSION: str
__doc__: str
__name__: str
__package__: str
_i_str: str

# =======
# <class 'builtin_function_or_method'>s
# =======

# =======
# # Document
# =======

def closeDoc() -> None: ...
def docChanged(changed: bool) -> None: ...
def docUnitToPoints(value: float) -> float: ...
def haveDoc() -> int: ...
@deprecated("Use NewDocument instead")
def newDoc(
    size: tuple[float, float],
    margins: tuple[float, float, float, float],
    orientation: int,
    firstPageNumber: int,
    unit: int,
    pagesType: int,
    firstPageOrder: int,
    numPages: int,
) -> bool: ...

newDoc.__doc__ = """
Creates a new document and returns true if successful. The parameters have the following meaning:

 * size = A tuple (width, height) describing the size of the document. You can use predefined constants named PAPER_ e.g. PAPER_A4 etc.
 * margins = A tuple (left, right, top, bottom) describing the document margins
 * orientation = the page orientation - constants PORTRAIT, LANDSCAPE

firstPageNumer = is the number of the first page in the document used for pagenumbering. While you'll usually want 1, it's useful to have higher numbers if you're creating a document in several parts.

unit: this value sets the measurement units used by the document. Use a predefined constant for this, one of: UNIT_INCHES, UNIT_MILLIMETERS, UNIT_PICAS, UNIT_POINTS.

pagesType = One of the predefined constants PAGE_n. PAGE_1 is single page, PAGE_2 is for facing pages documents, PAGE_3 is for 3 pages fold and PAGE_4 is 4-fold.

firstPageOrder = What is position of first page in the document. Indexed from 0 (0 = first).

numPage = Number of pages to be created.

The values for width, height and the margins are expressed in the given unit for the document. PAPER_ constants are expressed in points. If your document is not in points, make sure to account for this. Use UNIT_MM if you use PAPER_A_MM or PAPER_B*_MM constants. PAPER_A0_MM through PAPER_A9_MM and PAPER_B0_MM through PAPER_B10_MM are available.

example: newDocument(PAPER_A4, (10, 10, 20, 20), LANDSCAPE, 7, UNIT_POINTS, PAGE_4, 3, 1)

May raise ScribusError if is firstPageOrder bigger than allowed by pagesType.
"""

def newDocDialog() -> bool: ...  # TODO need to fill in return
def newDocument(
    size: tuple[float, float],
    margins: tuple[float, float, float, float],
    orientation: int,
    firstPageNumber: int,
    unit: int,
    pagesType: int,
    firstPageOrder: int,
    numPages: int,
) -> bool: ...

newDocument.__doc__ = """newDocument(...)
    newDocument(
        size, margins, orientation, firstPageNumber,
        unit, pagesType, firstPageOrder, numPages) -> bool

    Creates a new document and returns true if successful. The parameters have the following meaning:
        size = A tuple (width, height) describing the size of the document. You
            can use predefined constants named PAPER_<paper_type> e.g. PAPER_A4 etc.
        margins = A tuple (left, right, top, bottom) describing the document margins
        orientation = the page orientation - constants PORTRAIT, LANDSCAPE
        firstPageNumer = is the number of the first page in the document used
            for pagenumbering. While you'll usually want 1, it's useful to have
            higher numbers if you're creating a document in several parts.
        unit: this value sets the measurement units used by the document. Use a
            predefined constant for this, one of: UNIT_INCHES, UNIT_MILLIMETERS,
            UNIT_PICAS, UNIT_POINTS.
        pagesType = One of the predefined constants PAGE_n.
            PAGE_1 is single page,
            PAGE_2 is for facing pages documents,
            PAGE_3 is for 3 pages fold
            PAGE_4 is 4-fold.
        firstPageOrder = What is position of first page in the document.
            Indexed from 0 (0 = first).
        numPage = Number of pages to be created.

    The values for width, height and the margins are expressed in the given
    unit for the document. PAPER_* constants are expressed in points. If your
    document is not in points, make sure to account for this. Use UNIT_MM if
    you use PAPER_A*_MM or PAPER_B*_MM constants. PAPER_A0_MM through
    PAPER_A9_MM and PAPER_B0_MM through PAPER_B10_MM are available.

    example:
    ```
    newDocument(PAPER_A4, (10, 10, 20, 20), LANDSCAPE, 7, UNIT_POINTS, PAGE_4, 3, 1)
    ```

    May raise ScribusError if is firstPageOrder bigger than allowed by pagesType.

"""

def openDoc(name: str) -> None: ...  # TODO need to fill in return

# =======
# # Pages
# =======

def currentPage() -> int: ...
def currentPageNumber() -> int: ...
def getPageItems() -> list[tuple[str, int, int]]: ...

# getPageItems tuple: name, item type, order
def getPageMargins() -> tuple[float, float, float, float]: ...
def getPageNMargins() -> tuple[float, float, float, float]: ...
def getPageSize() -> tuple[float, float]: ...
def getPageNSize(pgNo: int) -> tuple[float, float]: ...
def getPageType() -> int: ...  # TODO constrain int return

# =======
# # MasterPages
# =======

def applyMasterPage(masterPageName: str, pageNumber: int) -> None: ...
def closeMasterPage() -> None: ...  # TODO need to fill in return
def createMasterPage(pageName: str) -> None: ...
def getMasterPage(pageNr: int) -> str: ...

# =======
# Layers
# =======

def createLayer(name: str) -> None: ...
def deleteLayer(name: str) -> None: ...
def getActiveLayer() -> str: ...
def getLayerBlendmode(layer: str) -> int: ...
def getLayerTransparency(layer: str) -> float: ...
def getLayers() -> list[str]: ...
def isLayerFlow(layer: str) -> bool: ...
def isLayerLocked(layer: str) -> bool: ...
def isLayerOutlined(layer: str) -> bool: ...
def isLayerPrintable(layer: str) -> bool: ...
def isLayerVisible(layer: str) -> bool: ...
def raiseActiveLayer() -> None: ...
def setLayerBlendmode(layer: str, blend: int) -> None: ...
def setLayerFlow(layer: str, flow: bool) -> None: ...
def setLayerLocked(layer: str, locked: bool) -> None: ...
def setLayerOutlined(layer: str, outlined: bool) -> None: ...
def setLayerPrintable(layer: str, printable: bool) -> None: ...
def setLayerTransparency(layer: str, trans: float) -> None: ...
def setLayerVisible(layer: str, visible: bool) -> None: ...
def sendToLayer(layer: str, name: str = "") -> None: ...
@deprecated("sentToLayer is deprecated, please use sendToLayer")
def sentToLayer(layer: str, name: str = "") -> None: ...
def setActiveLayer(layer: str) -> None: ...

# =======
# Frame Properties
# =======

def setLineCap() -> Any: ...  # TODO fill in return
def setLineColor() -> Any: ...  # TODO fill in return
def setLineJoin() -> Any: ...  # TODO fill in return
def setLineShade() -> Any: ...  # TODO fill in return
def setLineSpacing() -> Any: ...  # TODO fill in return
def setLineSpacingMode() -> Any: ...  # TODO fill in return
def setLineStyle() -> Any: ...  # TODO fill in return
def setLineTransparency() -> Any: ...  # TODO fill in return
def setLineWidth() -> Any: ...  # TODO fill in return

# =======
# # Item
# =======

def copyObject(object: str | None = None) -> None: ...
def copyObjects(objects: list[str] | None = None) -> None: ...
def createTable(
    x: float,
    y: float,
    width: float,
    height: float,
    numRows: int,
    numColumns: int,
    name: str = "",
) -> str: ...
def createText(
    x: float, y: float, width: float, height: float, name: str = ""
) -> str: ...
def createImage(
    x: float, y: float, width: float, height: float, name: str = ""
) -> str: ...
def moveSelectionToBack() -> None: ...
def moveSelectionToFront() -> None: ...
def pasteObject() -> str: ...
def pasteObjects() -> list[str]: ...
def selectObject() -> Any: ...  # TODO fill in return
def moveObject(
    dx: float, dy: float, name: str = ""
) -> Any: ...  # TODO fill in return
def moveObjectAbs(x: float, y: float, name: str = "") -> None: ...

# =======
# # Lines
# =======

def createBezierLine() -> Any: ...  # TODO fill in return
def createLine() -> Any: ...  # TODO fill in return
def createPolyLine(
    points: list[float | int], name: str | None = None
) -> str: ...  # TODO constraint len list to %2
def getLineStyle() -> Any: ...  # TODO fill in return

# =======
# # Shapes
# =======

def combinePolygons() -> Any: ...  # TODO fill in return
def createEllipse() -> Any: ...  # TODO fill in return
def createPolygon(
    points: list[float | int], name: str | None = None
) -> str: ...
def createRect(
    x: float | int,
    y: float | int,
    width: float | int,
    height: float | int,
    name: str | None,
) -> str: ...

# =======
# Tables
# =======

def getTableColumnWidth() -> Any: ...  # TODO fill in return
def getTableColumns() -> Any: ...  # TODO fill in return
def getTableFillColor() -> Any: ...  # TODO fill in return
def getTableRowHeight() -> Any: ...  # TODO fill in return
def getTableRows() -> Any: ...  # TODO fill in return
def getTableStyle() -> Any: ...  # TODO fill in return
def setTableBottomBorder() -> Any: ...  # TODO fill in return
def setTableFillColor() -> Any: ...  # TODO fill in return
def setTableLeftBorder() -> Any: ...  # TODO fill in return
def setTableRightBorder() -> Any: ...  # TODO fill in return
def setTableStyle() -> Any: ...  # TODO fill in return
def setTableTopBorder() -> Any: ...  # TODO fill in return

# =======
# ## Cell
# =======

def getCellColumnSpan() -> Any: ...  # TODO fill in return
def getCellFillColor() -> Any: ...  # TODO fill in return
def getCellRowSpan() -> Any: ...  # TODO fill in return
def getCellStyle() -> Any: ...  # TODO fill in return
def getCellText() -> Any: ...  # TODO fill in return
def setCellBottomBorder() -> Any: ...  # TODO fill in return
def setCellBottomPadding() -> Any: ...  # TODO fill in return
def setCellFillColor() -> Any: ...  # TODO fill in return
def setCellLeftBorder() -> Any: ...  # TODO fill in return
def setCellLeftPadding() -> Any: ...  # TODO fill in return
def setCellRightBorder() -> Any: ...  # TODO fill in return
def setCellRightPadding() -> Any: ...  # TODO fill in return
def setCellStyle() -> Any: ...  # TODO fill in return
def setCellText() -> Any: ...  # TODO fill in return
def setCellTopBorder() -> Any: ...  # TODO fill in return
def setCellTopPadding() -> Any: ...  # TODO fill in return

# =======
# # Style
# =======

def createCharStyle(
    name: str,
    font: str = "",
    fontsize: float = float(),
    features: str = "",
    fillcolor: str = "",
    fillshade: str = "",
    strokecolor: str = "",
    strokeshade: str = "",
    baselineoffset: float = 0.0,
    shadowxoffset: float = 0.0,
    shadowyoffset: float = 0.0,
    outlinewidth: float = 0.0,
    underlineoffset: float = 0.0,
    underlinewidth: float = 0.0,
    striketruoffset: float = 0.0,
    strikethruwidth: float = 0.0,
    scaleh: float = 1.0,
    scalev: float = 1.0,
    tracking: float = 0.0,
    language: str = "",
) -> ...: ...  # TODO need to fill in return
def createCustomLineStyle() -> Any: ...  # TODO fill in return
def createParagraphStyle(
    name: str,
    linespacingmode: int = 1,
    linespacing: float = 0.0,
    alignment: int = 0,
    leftmargin: float = 0.0,
    rightmargin: float = 0.0,
    gapbefore: float = 0.0,
    gapafter: float = 0.0,
    firstindent: float = 0.0,
    hasdropcap: int = 0,
    dropcaplines: int = 0,
    dropcapoffset: int = 0,
    charstyle: str = "",
    bullet: str = "",
    tabs: list[tuple[float] | tuple[float, int] | tuple[float, int, str]] = [],
) -> ...: ...  # TODO need to fill in return
def getLineStyles() -> Any: ...  # TODO fill in return
def getParagraphStyles() -> list[str]: ...  # TODO need to fill in return
def getCellStyles() -> Any: ...  # TODO fill in return
def getTableStyles() -> Any: ...  # TODO fill in return

# =======
# Color
# =======

def changeColor(name: str, c: int, m: int, y: int, k: int) -> None: ...
def changeColorCMYK(name: str, c: int, m: int, y: int, k: int) -> None: ...
def changeColorCMYKFloat(
    name: str, c: float, m: float, y: float, k: float
) -> None: ...
def changeColorLab(name: str, l: int, a: int, b: int) -> None: ...
def changeColorRGB(name: str, r: int, g: int, b: int) -> None: ...
def changeColorRGBFloat(name: str, r: float, g: float, b: float) -> None: ...
def defineColor() -> Any: ...  # TODO fill in return
def defineColorCMYK() -> Any: ...  # TODO fill in return
def defineColorCMYKFloat() -> Any: ...  # TODO fill in return
def defineColorLab() -> Any: ...  # TODO fill in return
def defineColorRGBFloat() -> Any: ...  # TODO fill in return
def getColor() -> Any: ...  # TODO fill in return
def getColorAsRGB() -> Any: ...  # TODO fill in return
def getColorAsRGBFloat() -> Any: ...  # TODO fill in return
def getColorFloat() -> Any: ...  # TODO fill in return
def getColorNames() -> Any: ...  # TODO fill in return

# =======
# # Misc
# =======
def createPathText() -> Any: ...  # TODO fill in return
def createPdfAnnotation() -> Any: ...  # TODO fill in return
def currentPageNumberForSection() -> Any: ...  # TODO fill in return
def dehyphenateText() -> Any: ...  # TODO fill in return
def deleteColor() -> Any: ...  # TODO fill in return
def deleteMasterPage() -> Any: ...  # TODO fill in return
def deleteObject() -> Any: ...  # TODO fill in return
def deletePage() -> Any: ...  # TODO fill in return
def deleteText() -> Any: ...  # TODO fill in return
def deselectAll() -> Any: ...  # TODO fill in return
def duplicateObject() -> Any: ...  # TODO fill in return
def duplicateObjects() -> Any: ...  # TODO fill in return
def editMasterPage(pageName: str) -> None: ...  # TODO need to fill in return
def fileDialog() -> Any: ...  # TODO fill in return
def fileQuit() -> Any: ...  # TODO fill in return
def flipObject() -> Any: ...  # TODO fill in return

# -1 is not a correct default for page, but I'm not sure I can replicate this
# well
def getAllObjects(
    type: int = -1, page: int = -1, layer: str = ""
) -> list[str]: ...
def getAllText() -> Any: ...  # TODO fill in return
def getBaseLine() -> Any: ...  # TODO fill in return
def getBleeds() -> Any: ...  # TODO fill in return
def getBoundingBox() -> Any: ...  # TODO fill in return
def getCharStyles() -> Any: ...  # TODO fill in return
def getCharacterStyle() -> Any: ...  # TODO fill in return
def getColumnGap() -> Any: ...  # TODO fill in return
def getColumnGuides() -> Any: ...  # TODO fill in return
def getColumns() -> Any: ...  # TODO fill in return
def getCornerRadius() -> Any: ...  # TODO fill in return
def getCurrentPageSize() -> Any: ...  # TODO fill in return
def getCustomLineStyle() -> Any: ...  # TODO fill in return
def getDocName() -> str: ...
def getFillBlendmode() -> Any: ...  # TODO fill in return
def getFillColor() -> Any: ...  # TODO fill in return
def getFillShade() -> Any: ...  # TODO fill in return
def getFillTransparency() -> Any: ...  # TODO fill in return
def getFirstLineOffset() -> Any: ...  # TODO fill in return
def getFirstLinkedFrame() -> Any: ...  # TODO fill in return
def getFont() -> Any: ...  # TODO fill in return
def getFontFeatures() -> Any: ...  # TODO fill in return
def getFontNames() -> Any: ...  # TODO fill in return
def getFontSize() -> Any: ...  # TODO fill in return
def getFrameSelectedTextRange() -> Any: ...  # TODO fill in return
def getText() -> Any: ...  # TODO fill in return
def getGradientStop() -> Any: ...  # TODO fill in return
def getGradientStopsCount() -> Any: ...  # TODO fill in return
def getGradientVector() -> Any: ...  # TODO fill in return
def getGroupItems() -> Any: ...  # TODO fill in return
def getGuiLanguage() -> Any: ...  # TODO fill in return
def getHGuides() -> Any: ...  # TODO fill in return
def getImageColorSpace() -> Any: ...  # TODO fill in return
def getImageFile() -> Any: ...  # TODO fill in return
def getImageOffset() -> Any: ...  # TODO fill in return
def getImagePage() -> Any: ...  # TODO fill in return
def getImagePageCount() -> Any: ...  # TODO fill in return
def getImagePpi() -> Any: ...  # TODO fill in return
def getImagePreviewResolution() -> Any: ...  # TODO fill in return
def getImageScale() -> Any: ...  # TODO fill in return
def getInfo() -> Any: ...  # TODO fill in return
def getItemPageNumber(name: str) -> int: ...
def getJSActionScript() -> Any: ...  # TODO fill in return
def getLastLinkedFrame() -> Any: ...  # TODO fill in return
def getLineBlendmode() -> Any: ...  # TODO fill in return
def getLineCap() -> Any: ...  # TODO fill in return
def getLineColor() -> Any: ...  # TODO fill in return
def getLineJoin() -> Any: ...  # TODO fill in return
def getLineShade() -> Any: ...  # TODO fill in return
def getLineSpacing() -> Any: ...  # TODO fill in return
def getLineSpacingMode() -> Any: ...  # TODO fill in return
def getLineTransparency() -> Any: ...  # TODO fill in return
def getLineWidth() -> Any: ...  # TODO fill in return
def getMargins() -> Any: ...  # TODO fill in return
def getMinWordTracking() -> Any: ...  # TODO fill in return
def getNextLinkedFrame() -> Any: ...  # TODO fill in return
def getObjectAttributes() -> Any: ...  # TODO fill in return
def getObjectType() -> Any: ...  # TODO fill in return
def getPageNSize(nr: int) -> tuple[float, float]: ...
def pageDimension() -> tuple[float, float]: ...
def getStyle(objectName: str = "") -> str | None: ...
def getPosition() -> Any: ...  # TODO fill in return
def getPrevLinkedFrame() -> Any: ...  # TODO fill in return
def getProperty() -> Any: ...  # TODO fill in return
def getPropertyCType() -> Any: ...  # TODO fill in return
def getPropertyNames() -> Any: ...  # TODO fill in return
def getRotation() -> Any: ...  # TODO fill in return
def getRowGuides() -> Any: ...  # TODO fill in return
def getSelectedObject() -> str: ...
def getSelectedTextRange() -> Any: ...  # TODO fill in return
def getSize() -> tuple[float, float]: ...
def getTextColor() -> Any: ...  # TODO fill in return
def getTextDistances() -> Any: ...  # TODO fill in return
def getTextFlowMode() -> Any: ...  # TODO fill in return
def getTextLength(texObj: str = "") -> int: ...
def getTextLines() -> Any: ...  # TODO fill in return
def getTextShade() -> Any: ...  # TODO fill in return
def getTextVerticalAlignment() -> Any: ...  # TODO fill in return
def getTracking() -> Any: ...  # TODO fill in return
def getUnit() -> Any: ...  # TODO fill in return
def getVGuides() -> Any: ...  # TODO fill in return
def getVisualBoundingBox() -> Any: ...  # TODO fill in return
def getWordTracking() -> Any: ...  # TODO fill in return
def getXFontNames() -> Any: ...  # TODO fill in return
def getval() -> Any: ...  # TODO fill in return
def gotoPage(pageNr: int) -> None: ...  # TODO need to fill in return
def groupObjects(objects: list[str]) -> Any: ...  # TODO fill in return
def hyphenateText() -> Any: ...  # TODO fill in return
def importPage() -> Any: ...  # TODO fill in return
def insertHtmlText() -> Any: ...  # TODO fill in return
def insertTableColumns() -> Any: ...  # TODO fill in return
def insertTableRows() -> Any: ...  # TODO fill in return
def insertText() -> Any: ...  # TODO fill in return
def isAnnotated() -> Any: ...  # TODO fill in return
def isExportable() -> Any: ...  # TODO fill in return
def isLocked() -> Any: ...  # TODO fill in return
def isPDFBookmark() -> Any: ...  # TODO fill in return
def isSpotColor() -> Any: ...  # TODO fill in return
def itemDialog() -> Any: ...  # TODO fill in return
def layoutText() -> Any: ...  # TODO fill in return
def layoutTextChain() -> Any: ...  # TODO fill in return
def linkTextFrames() -> Any: ...  # TODO fill in return
def loadImage() -> Any: ...  # TODO fill in return
def loadStylesFromFile() -> Any: ...  # TODO fill in return
def lockObject() -> Any: ...  # TODO fill in return
def lowerActiveLayer() -> Any: ...  # TODO fill in return
def masterPageNames() -> list[str]: ...
def mergeTableCells(
    row: int,
    column: int,
    numRows: int,
    numColumns: int,
    name: str | None = None,
) -> None: ...
def messageBox() -> Any: ...  # TODO fill in return
def statusMessage() -> Any: ...  # TODO fill in return
def newPage(where: int, masterPage: str = "") -> None: ...
def newStyleDialog() -> Any: ...  # TODO fill in return
def objectExists() -> Any: ...  # TODO fill in return
def traceText() -> Any: ...  # TODO fill in return
def pageCount() -> int: ...
def placeVectorFile() -> Any: ...  # TODO fill in return
def pointsToDocUnit() -> Any: ...  # TODO fill in return
def progressReset() -> Any: ...  # TODO fill in return
def progressSet(progress: float) -> Any: ...  # TODO fill in return
def progressTotal() -> Any: ...  # TODO fill in return
def readPDFOptions() -> Any: ...  # TODO fill in return
def redrawAll() -> Any: ...  # TODO fill in return
def removeTableColumns() -> Any: ...  # TODO fill in return
def removeTableRows() -> Any: ...  # TODO fill in return
def renderFont() -> Any: ...  # TODO fill in return
def replaceColor() -> Any: ...  # TODO fill in return
def resizeTableColumn() -> Any: ...  # TODO fill in return
def resizeTableRow() -> Any: ...  # TODO fill in return
def retval() -> Any: ...  # TODO fill in return
def revertDoc() -> Any: ...  # TODO fill in return
def rotateObject() -> Any: ...  # TODO fill in return
def setRotation() -> Any: ...  # TODO fill in return
def saveDoc() -> None: ...
def saveDocAs(newName: str) -> None: ...
def savePDFOptions() -> Any: ...  # TODO fill in return
def savePageAsEPS() -> Any: ...  # TODO fill in return
def scaleGroup(factor: float, name: str = "") -> None: ...
def scaleImage() -> Any: ...  # TODO fill in return
def scrollDocument() -> Any: ...  # TODO fill in return
def selectFrameText() -> Any: ...  # TODO fill in return
def selectText() -> Any: ...  # TODO fill in return
def selectionCount() -> Any: ...  # TODO fill in return
def setBaseLine() -> Any: ...  # TODO fill in return
def setBleeds() -> Any: ...  # TODO fill in return
def setCharacterStyle() -> Any: ...  # TODO fill in return
def setColumnGap() -> Any: ...  # TODO fill in return
def setColumnGuides() -> Any: ...  # TODO fill in return
def setColumns() -> Any: ...  # TODO fill in return
def setCornerRadius() -> Any: ...  # TODO fill in return
def setCurrentPageSize() -> Any: ...  # TODO fill in return
def setCursor() -> Any: ...  # TODO fill in return
def setCustomLineStyle() -> Any: ...  # TODO fill in return
def setDocType(
    facingPages: int, firstPageLeft: int
) -> None: ...  # TODO need to fill in return
def setEditMode() -> Any: ...  # TODO fill in return
def setExportableObject() -> Any: ...  # TODO fill in return
def setFileAnnotation() -> Any: ...  # TODO fill in return
def setFillBlendmode() -> Any: ...  # TODO fill in return
def setFillColor() -> Any: ...  # TODO fill in return
def setFillShade() -> Any: ...  # TODO fill in return
def setFillTransparency() -> Any: ...  # TODO fill in return
def setFirstLineOffset() -> Any: ...  # TODO fill in return
def setFont(fontName: str, textObj: str = "") -> None: ...
def setFontFeatures() -> Any: ...  # TODO fill in return
def setFontSize() -> Any: ...  # TODO fill in return
def setGradientFill() -> Any: ...  # TODO fill in return
def setGradientStop() -> Any: ...  # TODO fill in return
def setGradientVector() -> Any: ...  # TODO fill in return
def setHGuides() -> Any: ...  # TODO fill in return
def setImageBrightness() -> Any: ...  # TODO fill in return
def setImageGrayscale() -> Any: ...  # TODO fill in return
def setImageOffset() -> Any: ...  # TODO fill in return
def setImagePage() -> Any: ...  # TODO fill in return
def setImagePreviewResolution() -> Any: ...  # TODO fill in return
def setImageScale() -> Any: ...  # TODO fill in return
def setInfo() -> Any: ...  # TODO fill in return
def setItemName(newName: str, name: str = "") -> str: ...
def setNewName(newName: str, name: str = "") -> str: ...
def setJSActionScript() -> Any: ...  # TODO fill in return
def setLineBlendmode() -> Any: ...  # TODO fill in return
def setLinkAnnotation() -> Any: ...  # TODO fill in return
def setMargins() -> Any: ...  # TODO fill in return
def setMinWordTracking() -> Any: ...  # TODO fill in return
def setMultiLine() -> Any: ...  # TODO fill in return
def setNormalMode() -> Any: ...  # TODO fill in return
def setObjectAttributes() -> Any: ...  # TODO fill in return
def setPDFBookmark() -> Any: ...  # TODO fill in return
def setStyle() -> Any: ...  # TODO fill in return
def setProperty() -> Any: ...  # TODO fill in return
def setRedraw(redraw: bool) -> None: ...  # TODO need to fill in return
def setRowGuides() -> Any: ...  # TODO fill in return
def setScaleFrameToImage() -> Any: ...  # TODO fill in return
def setScaleImageToFrame() -> Any: ...  # TODO fill in return
def setSpotColor() -> Any: ...  # TODO fill in return
def setText() -> Any: ...  # TODO fill in return
def setTextAlignment() -> Any: ...  # TODO fill in return
def setTextAnnotation() -> Any: ...  # TODO fill in return
def setTextColor() -> Any: ...  # TODO fill in return
def setTextDirection() -> Any: ...  # TODO fill in return
def setTextDistances() -> Any: ...  # TODO fill in return
def textFlowMode() -> Any: ...  # TODO fill in return
def setTextScalingH() -> Any: ...  # TODO fill in return
def setTextScalingV() -> Any: ...  # TODO fill in return
def setTextShade() -> Any: ...  # TODO fill in return
def setTextStroke() -> Any: ...  # TODO fill in return
def setTextVerticalAlignment() -> Any: ...  # TODO fill in return
def setTracking() -> Any: ...  # TODO fill in return
def setURIAnnotation() -> Any: ...  # TODO fill in return
def setUnit() -> Any: ...  # TODO fill in return
def setVGuides() -> Any: ...  # TODO fill in return
def setWordTracking() -> Any: ...  # TODO fill in return
def sizeObject() -> Any: ...  # TODO fill in return
def stringValueToPoints() -> Any: ...  # TODO fill in return
def textOverflows() -> Any: ...  # TODO fill in return
def unGroupObjects() -> Any: ...  # TODO fill in return
def unlinkTextFrames() -> Any: ...  # TODO fill in return
def valueDialog() -> Any: ...  # TODO fill in return
def zoomDocument(double: float) -> Any: ...  # TODO fill in return

# =======
# <class 'float'>s
# =======

c: float
cm: float
inch: float
mm: float
pt: float
# =======
# <class 'bool'>s
# =======

mainInterpreter: bool
# =======
# PyCapsules
# =======

mainWindow: CapsuleType
qApp: CapsuleType
