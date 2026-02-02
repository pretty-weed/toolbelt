from types import CapsuleType
from typing import Any, Self, SupportsIndex, override

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
    def __reduce_ex__(self, protocol: SupportsIndex) -> tuple[Any, ...]: ... # TODO this could be more explicit return
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
    # file: <class 'getset_descriptor'>
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
    def save(self): ...
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
    def __init__(self, *args: Any, **kwargs: Any): ...
    def __init_subclass__(cls) -> None: ...
    def __le__(self: Self, value: Any) -> bool: ...
    def __lt__(self: Self, value: Any) -> bool: ...
    @override
    def __ne__(self: Self, value: Any) -> bool: ...
    def __new__(cls: object, *args: Any, **kwargs: Any) -> object: ...
    @override
    def __reduce__(self) -> tuple[Any, ...]: ...
    def __reduce_ex__(self, protocol: SupportsIndex) -> tuple[Any, ...]: ... # TODO this could be more explicit return
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

def applyMasterPage(masterPageName: str, pageNumber: int) -> None: ...
def changeColor(name: str, c: int, m: int, y: int, k: int) -> None: ...
def changeColorCMYK(name: str, c: int, m: int, y: int, k: int) -> None: ... 
def changeColorCMYKFloat(name: str, c: float, m: float, y: float, k: float) -> None: ...
def changeColorLab(name: str, l: int, a: int, b: int) -> None: ...  
def changeColorRGB(name: str, r: int, g: int, b: int) -> None: ...  
def changeColorRGBFloat(name: str, r: float, g: float, b: float) -> None: ...
def closeDoc() -> ...: ...  # TODO need to fill in return
def closeMasterPage() -> ...: ...  # TODO need to fill in return
def combinePolygons() -> ...: ...  # TODO need to fill in return
def copyObject() -> ...: ...  # TODO need to fill in return
def copyObjects(objects: list[str]) -> ...: ...  # TODO need to fill in return
def createBezierLine() -> ...: ...  # TODO need to fill in return
def createCharStyle() -> ...: ...  # TODO need to fill in return
def createCustomLineStyle() -> ...: ...  # TODO need to fill in return
def createEllipse() -> ...: ...  # TODO need to fill in return
def createImage() -> ...: ...  # TODO need to fill in return
def createLayer() -> ...: ...  # TODO need to fill in return
def createLine() -> ...: ...  # TODO need to fill in return
def createMasterPage(pageName: str) -> None: ...  
def createParagraphStyle() -> ...: ...  # TODO need to fill in return
def createPathText() -> ...: ...  # TODO need to fill in return
def createPdfAnnotation() -> ...: ...  # TODO need to fill in return
def createPolyLine(points: list[float | int], name: str | None = None) -> str: ...  # TODO constraint len list to %2
def createPolygon(points: list[float | int], name: str | None = None) -> str: ...
def createRect(x: float | int, y: float | int, width: float | int, height: float | int, name: str | None) -> str: ...
def createTable() -> ...: ...  # TODO need to fill in return
def createText() -> ...: ...  # TODO need to fill in return
def currentPageNumber() -> ...: ...  # TODO need to fill in return
def currentPageNumberForSection() -> ...: ...  # TODO need to fill in return
def defineColor() -> ...: ...  # TODO need to fill in return
def defineColorCMYK() -> ...: ...  # TODO need to fill in return
def defineColorCMYKFloat() -> ...: ...  # TODO need to fill in return
def defineColorLab() -> ...: ...  # TODO need to fill in return
def defineColorRGBFloat() -> ...: ...  # TODO need to fill in return
def dehyphenateText() -> ...: ...  # TODO need to fill in return
def deleteColor() -> ...: ...  # TODO need to fill in return
def deleteLayer() -> ...: ...  # TODO need to fill in return
def deleteMasterPage() -> ...: ...  # TODO need to fill in return
def deleteObject() -> ...: ...  # TODO need to fill in return
def deletePage() -> ...: ...  # TODO need to fill in return
def deleteText() -> ...: ...  # TODO need to fill in return
def deselectAll() -> ...: ...  # TODO need to fill in return
def docChanged() -> ...: ...  # TODO need to fill in return
def docUnitToPoints() -> ...: ...  # TODO need to fill in return
def duplicateObject() -> ...: ...  # TODO need to fill in return
def duplicateObjects() -> ...: ...  # TODO need to fill in return
def editMasterPage(pageName: str) -> None: ...  # TODO need to fill in return
def fileDialog() -> ...: ...  # TODO need to fill in return
def fileQuit() -> ...: ...  # TODO need to fill in return
def flipObject() -> ...: ...  # TODO need to fill in return
def getActiveLayer() -> ...: ...  # TODO need to fill in return

# -1 is not a correct default for page, but I'm not sure I can replicate this
# well
def getAllObjects(type: int = -1, page: int = -1, layer: str = "") -> list[str]: ...
def getParagraphStyles() -> list[str]: ...  # TODO need to fill in return
def getAllText() -> ...: ...  # TODO need to fill in return
def getBaseLine() -> ...: ...  # TODO need to fill in return
def getBleeds() -> ...: ...  # TODO need to fill in return
def getBoundingBox() -> ...: ...  # TODO need to fill in return
def getCellColumnSpan() -> ...: ...  # TODO need to fill in return
def getCellFillColor() -> ...: ...  # TODO need to fill in return
def getCellRowSpan() -> ...: ...  # TODO need to fill in return
def getCellStyle() -> ...: ...  # TODO need to fill in return
def getCellStyles() -> ...: ...  # TODO need to fill in return
def getCellText() -> ...: ...  # TODO need to fill in return
def getCharStyles() -> ...: ...  # TODO need to fill in return
def getCharacterStyle() -> ...: ...  # TODO need to fill in return
def getColor() -> ...: ...  # TODO need to fill in return
def getColorAsRGB() -> ...: ...  # TODO need to fill in return
def getColorAsRGBFloat() -> ...: ...  # TODO need to fill in return
def getColorFloat() -> ...: ...  # TODO need to fill in return
def getColorNames() -> ...: ...  # TODO need to fill in return
def getColumnGap() -> ...: ...  # TODO need to fill in return
def getColumnGuides() -> ...: ...  # TODO need to fill in return
def getColumns() -> ...: ...  # TODO need to fill in return
def getCornerRadius() -> ...: ...  # TODO need to fill in return
def getCurrentPageSize() -> ...: ...  # TODO need to fill in return
def getCustomLineStyle() -> ...: ...  # TODO need to fill in return
def getDocName() -> str: ...
def getFillBlendmode() -> ...: ...  # TODO need to fill in return
def getFillColor() -> ...: ...  # TODO need to fill in return
def getFillShade() -> ...: ...  # TODO need to fill in return
def getFillTransparency() -> ...: ...  # TODO need to fill in return
def getFirstLineOffset() -> ...: ...  # TODO need to fill in return
def getFirstLinkedFrame() -> ...: ...  # TODO need to fill in return
def getFont() -> ...: ...  # TODO need to fill in return
def getFontFeatures() -> ...: ...  # TODO need to fill in return
def getFontNames() -> ...: ...  # TODO need to fill in return
def getFontSize() -> ...: ...  # TODO need to fill in return
def getFrameSelectedTextRange() -> ...: ...  # TODO need to fill in return
def getText() -> ...: ...  # TODO need to fill in return
def getGradientStop() -> ...: ...  # TODO need to fill in return
def getGradientStopsCount() -> ...: ...  # TODO need to fill in return
def getGradientVector() -> ...: ...  # TODO need to fill in return
def getGroupItems() -> ...: ...  # TODO need to fill in return
def getGuiLanguage() -> ...: ...  # TODO need to fill in return
def getHGuides() -> ...: ...  # TODO need to fill in return
def getImageColorSpace() -> ...: ...  # TODO need to fill in return
def getImageFile() -> ...: ...  # TODO need to fill in return
def getImageOffset() -> ...: ...  # TODO need to fill in return
def getImagePage() -> ...: ...  # TODO need to fill in return
def getImagePageCount() -> ...: ...  # TODO need to fill in return
def getImagePpi() -> ...: ...  # TODO need to fill in return
def getImagePreviewResolution() -> ...: ...  # TODO need to fill in return
def getImageScale() -> ...: ...  # TODO need to fill in return
def getInfo() -> ...: ...  # TODO need to fill in return
def getItemPageNumber() -> ...: ...  # TODO need to fill in return
def getJSActionScript() -> ...: ...  # TODO need to fill in return
def getLastLinkedFrame() -> ...: ...  # TODO need to fill in return
def getLayerBlendmode() -> ...: ...  # TODO need to fill in return
def getLayerTransparency() -> ...: ...  # TODO need to fill in return
def getLayers() -> ...: ...  # TODO need to fill in return
def getLineBlendmode() -> ...: ...  # TODO need to fill in return
def getLineCap() -> ...: ...  # TODO need to fill in return
def getLineColor() -> ...: ...  # TODO need to fill in return
def getLineJoin() -> ...: ...  # TODO need to fill in return
def getLineShade() -> ...: ...  # TODO need to fill in return
def getLineSpacing() -> ...: ...  # TODO need to fill in return
def getLineSpacingMode() -> ...: ...  # TODO need to fill in return
def getLineStyle() -> ...: ...  # TODO need to fill in return
def getLineStyles() -> ...: ...  # TODO need to fill in return
def getLineTransparency() -> ...: ...  # TODO need to fill in return
def getLineWidth() -> ...: ...  # TODO need to fill in return
def getMargins() -> ...: ...  # TODO need to fill in return
def getMasterPage(pageNr: int) -> str : ... 
def getMinWordTracking() -> ...: ...  # TODO need to fill in return
def getNextLinkedFrame() -> ...: ...  # TODO need to fill in return
def getObjectAttributes() -> ...: ...  # TODO need to fill in return
def getObjectType() -> ...: ...  # TODO need to fill in return
def getPageItems() -> ...: ...  # TODO need to fill in return
def getPageMargins() -> ...: ...  # TODO need to fill in return
def getPageNMargins() -> ...: ...  # TODO need to fill in return
def getPageNSize() -> tuple[float, float]: ...
def pageDimension() -> tuple[float, float]: ...
def getPageType() -> ...: ...  # TODO need to fill in return
def getStyle(objectName: str = "") -> str | None: ...
def getPosition() -> ...: ...  # TODO need to fill in return
def getPrevLinkedFrame() -> ...: ...  # TODO need to fill in return
def getProperty() -> ...: ...  # TODO need to fill in return
def getPropertyCType() -> ...: ...  # TODO need to fill in return
def getPropertyNames() -> ...: ...  # TODO need to fill in return
def getRotation() -> ...: ...  # TODO need to fill in return
def getRowGuides() -> ...: ...  # TODO need to fill in return
def getSelectedObject() -> ...: ...  # TODO need to fill in return
def getSelectedTextRange() -> ...: ...  # TODO need to fill in return
def getSize() -> ...: ...  # TODO need to fill in return
def getTableColumnWidth() -> ...: ...  # TODO need to fill in return
def getTableColumns() -> ...: ...  # TODO need to fill in return
def getTableFillColor() -> ...: ...  # TODO need to fill in return
def getTableRowHeight() -> ...: ...  # TODO need to fill in return
def getTableRows() -> ...: ...  # TODO need to fill in return
def getTableStyle() -> ...: ...  # TODO need to fill in return
def getTableStyles() -> ...: ...  # TODO need to fill in return
def getTextColor() -> ...: ...  # TODO need to fill in return
def getTextDistances() -> ...: ...  # TODO need to fill in return
def getTextFlowMode() -> ...: ...  # TODO need to fill in return
def getTextLength(texObj: str = "") -> int: ...
def getTextLines() -> ...: ...  # TODO need to fill in return
def getTextShade() -> ...: ...  # TODO need to fill in return
def getTextVerticalAlignment() -> ...: ...  # TODO need to fill in return
def getTracking() -> ...: ...  # TODO need to fill in return
def getUnit() -> ...: ...  # TODO need to fill in return
def getVGuides() -> ...: ...  # TODO need to fill in return
def getVisualBoundingBox() -> ...: ...  # TODO need to fill in return
def getWordTracking() -> ...: ...  # TODO need to fill in return
def getXFontNames() -> ...: ...  # TODO need to fill in return
def getval() -> ...: ...  # TODO need to fill in return
def gotoPage(pageNr: int) -> None: ...  # TODO need to fill in return
def groupObjects(objects: list[str]) -> str: ...  # TODO need to fill in return
def haveDoc() -> ...: ...  # TODO need to fill in return
def hyphenateText() -> ...: ...  # TODO need to fill in return
def importPage() -> ...: ...  # TODO need to fill in return
def insertHtmlText() -> ...: ...  # TODO need to fill in return
def insertTableColumns() -> ...: ...  # TODO need to fill in return
def insertTableRows() -> ...: ...  # TODO need to fill in return
def insertText() -> ...: ...  # TODO need to fill in return
def isAnnotated() -> ...: ...  # TODO need to fill in return
def isExportable() -> ...: ...  # TODO need to fill in return
def isLayerFlow() -> ...: ...  # TODO need to fill in return
def isLayerLocked() -> ...: ...  # TODO need to fill in return
def isLayerOutlined() -> ...: ...  # TODO need to fill in return
def isLayerPrintable() -> ...: ...  # TODO need to fill in return
def isLayerVisible() -> ...: ...  # TODO need to fill in return
def isLocked() -> ...: ...  # TODO need to fill in return
def isPDFBookmark() -> ...: ...  # TODO need to fill in return
def isSpotColor() -> ...: ...  # TODO need to fill in return
def itemDialog() -> ...: ...  # TODO need to fill in return
def layoutText() -> ...: ...  # TODO need to fill in return
def layoutTextChain() -> ...: ...  # TODO need to fill in return
def linkTextFrames() -> ...: ...  # TODO need to fill in return
def loadImage() -> ...: ...  # TODO need to fill in return
def loadStylesFromFile() -> ...: ...  # TODO need to fill in return
def lockObject() -> ...: ...  # TODO need to fill in return
def lowerActiveLayer() -> ...: ...  # TODO need to fill in return
def masterPageNames() -> list[str]: ...
def mergeTableCells(row: int, column: int, numRows: int, numColumns: int, name: str | None = None) -> None: ...
def messageBox() -> ...: ...  # TODO need to fill in return
def statusMessage() -> ...: ...  # TODO need to fill in return
def moveObject() -> ...: ...  # TODO need to fill in return
def moveObjectAbs(x: float, y: float, name: str = "") -> None: ... 
def moveSelectionToBack() -> ...: ...  # TODO need to fill in return
def moveSelectionToFront() -> ...: ...  # TODO need to fill in return
def newDoc() -> ...: ...  # TODO need to fill in return
def newDocDialog() -> ...: ...  # TODO need to fill in return
def newDocument() -> ...: ...  # TODO need to fill in return
def newPage(where: int, masterPage: str = "") -> None: ...
def newStyleDialog() -> ...: ...  # TODO need to fill in return
def objectExists() -> ...: ...  # TODO need to fill in return
def openDoc() -> ...: ...  # TODO need to fill in return
def traceText() -> ...: ...  # TODO need to fill in return
def pageCount() -> int: ...
def pasteObject() -> str: ... 
def pasteObjects() -> list[str]: ...
def placeVectorFile() -> ...: ...  # TODO need to fill in return
def pointsToDocUnit() -> ...: ...  # TODO need to fill in return
def progressReset() -> ...: ...  # TODO need to fill in return
def progressSet() -> ...: ...  # TODO need to fill in return
def progressTotal() -> ...: ...  # TODO need to fill in return
def raiseActiveLayer() -> ...: ...  # TODO need to fill in return
def readPDFOptions() -> ...: ...  # TODO need to fill in return
def redrawAll() -> ...: ...  # TODO need to fill in return
def removeTableColumns() -> ...: ...  # TODO need to fill in return
def removeTableRows() -> ...: ...  # TODO need to fill in return
def renderFont() -> ...: ...  # TODO need to fill in return
def replaceColor() -> ...: ...  # TODO need to fill in return
def resizeTableColumn() -> ...: ...  # TODO need to fill in return
def resizeTableRow() -> ...: ...  # TODO need to fill in return
def retval() -> ...: ...  # TODO need to fill in return
def revertDoc() -> ...: ...  # TODO need to fill in return
def rotateObject() -> ...: ...  # TODO need to fill in return
def setRotation() -> ...: ...  # TODO need to fill in return
def saveDoc() -> ...: ...  # TODO need to fill in return
def saveDocAs(newName: str) -> None: ...
def savePDFOptions() -> ...: ...  # TODO need to fill in return
def savePageAsEPS() -> ...: ...  # TODO need to fill in return
def scaleGroup(factor: float, name: str = "") -> None ...  
def scaleImage() -> ...: ...  # TODO need to fill in return
def scrollDocument() -> ...: ...  # TODO need to fill in return
def selectFrameText() -> ...: ...  # TODO need to fill in return
def selectObject() -> ...: ...  # TODO need to fill in return
def selectText() -> ...: ...  # TODO need to fill in return
def selectionCount() -> ...: ...  # TODO need to fill in return
def sentToLayer() -> ...: ...  # TODO need to fill in return
def setActiveLayer() -> ...: ...  # TODO need to fill in return
def setBaseLine() -> ...: ...  # TODO need to fill in return
def setBleeds() -> ...: ...  # TODO need to fill in return
def setCellBottomBorder() -> ...: ...  # TODO need to fill in return
def setCellBottomPadding() -> ...: ...  # TODO need to fill in return
def setCellFillColor() -> ...: ...  # TODO need to fill in return
def setCellLeftBorder() -> ...: ...  # TODO need to fill in return
def setCellLeftPadding() -> ...: ...  # TODO need to fill in return
def setCellRightBorder() -> ...: ...  # TODO need to fill in return
def setCellRightPadding() -> ...: ...  # TODO need to fill in return
def setCellStyle() -> ...: ...  # TODO need to fill in return
def setCellText() -> ...: ...  # TODO need to fill in return
def setCellTopBorder() -> ...: ...  # TODO need to fill in return
def setCellTopPadding() -> ...: ...  # TODO need to fill in return
def setCharacterStyle() -> ...: ...  # TODO need to fill in return
def setColumnGap() -> ...: ...  # TODO need to fill in return
def setColumnGuides() -> ...: ...  # TODO need to fill in return
def setColumns() -> ...: ...  # TODO need to fill in return
def setCornerRadius() -> ...: ...  # TODO need to fill in return
def setCurrentPageSize() -> ...: ...  # TODO need to fill in return
def setCursor() -> ...: ...  # TODO need to fill in return
def setCustomLineStyle() -> ...: ...  # TODO need to fill in return
def setDocType(facingPages: int, firstPageLeft: int) -> None: ...  # TODO need to fill in return
def setEditMode() -> ...: ...  # TODO need to fill in return
def setExportableObject() -> ...: ...  # TODO need to fill in return
def setFileAnnotation() -> ...: ...  # TODO need to fill in return
def setFillBlendmode() -> ...: ...  # TODO need to fill in return
def setFillColor() -> ...: ...  # TODO need to fill in return
def setFillShade() -> ...: ...  # TODO need to fill in return
def setFillTransparency() -> ...: ...  # TODO need to fill in return
def setFirstLineOffset() -> ...: ...  # TODO need to fill in return
def setFont(fontName: str, textObj: str = "") -> None: ... 
def setFontFeatures() -> ...: ...  # TODO need to fill in return
def setFontSize() -> ...: ...  # TODO need to fill in return
def setGradientFill() -> ...: ...  # TODO need to fill in return
def setGradientStop() -> ...: ...  # TODO need to fill in return
def setGradientVector() -> ...: ...  # TODO need to fill in return
def setHGuides() -> ...: ...  # TODO need to fill in return
def setImageBrightness() -> ...: ...  # TODO need to fill in return
def setImageGrayscale() -> ...: ...  # TODO need to fill in return
def setImageOffset() -> ...: ...  # TODO need to fill in return
def setImagePage() -> ...: ...  # TODO need to fill in return
def setImagePreviewResolution() -> ...: ...  # TODO need to fill in return
def setImageScale() -> ...: ...  # TODO need to fill in return
def setInfo() -> ...: ...  # TODO need to fill in return
def setItemName(newName: str, name: str = "") -> str: ...
def setNewName() -> ...: ...  # TODO need to fill in return
def setJSActionScript() -> ...: ...  # TODO need to fill in return
def setLayerBlendmode() -> ...: ...  # TODO need to fill in return
def setLayerFlow() -> ...: ...  # TODO need to fill in return
def setLayerLocked() -> ...: ...  # TODO need to fill in return
def setLayerOutlined() -> ...: ...  # TODO need to fill in return
def setLayerPrintable() -> ...: ...  # TODO need to fill in return
def setLayerTransparency() -> ...: ...  # TODO need to fill in return
def setLayerVisible() -> ...: ...  # TODO need to fill in return
def setLineBlendmode() -> ...: ...  # TODO need to fill in return
def setLineCap() -> ...: ...  # TODO need to fill in return
def setLineColor() -> ...: ...  # TODO need to fill in return
def setLineJoin() -> ...: ...  # TODO need to fill in return
def setLineShade() -> ...: ...  # TODO need to fill in return
def setLineSpacing() -> ...: ...  # TODO need to fill in return
def setLineSpacingMode() -> ...: ...  # TODO need to fill in return
def setLineStyle() -> ...: ...  # TODO need to fill in return
def setLineTransparency() -> ...: ...  # TODO need to fill in return
def setLineWidth() -> ...: ...  # TODO need to fill in return
def setLinkAnnotation() -> ...: ...  # TODO need to fill in return
def setMargins() -> ...: ...  # TODO need to fill in return
def setMinWordTracking() -> ...: ...  # TODO need to fill in return
def setMultiLine() -> ...: ...  # TODO need to fill in return
def setNormalMode() -> ...: ...  # TODO need to fill in return
def setObjectAttributes() -> ...: ...  # TODO need to fill in return
def setPDFBookmark() -> ...: ...  # TODO need to fill in return
def setStyle() -> ...: ...  # TODO need to fill in return
def setProperty() -> ...: ...  # TODO need to fill in return
def setRedraw() -> ...: ...  # TODO need to fill in return
def setRowGuides() -> ...: ...  # TODO need to fill in return
def setScaleFrameToImage() -> ...: ...  # TODO need to fill in return
def setScaleImageToFrame() -> ...: ...  # TODO need to fill in return
def setSpotColor() -> ...: ...  # TODO need to fill in return
def setTableBottomBorder() -> ...: ...  # TODO need to fill in return
def setTableFillColor() -> ...: ...  # TODO need to fill in return
def setTableLeftBorder() -> ...: ...  # TODO need to fill in return
def setTableRightBorder() -> ...: ...  # TODO need to fill in return
def setTableStyle() -> ...: ...  # TODO need to fill in return
def setTableTopBorder() -> ...: ...  # TODO need to fill in return
def setText() -> ...: ...  # TODO need to fill in return
def setTextAlignment() -> ...: ...  # TODO need to fill in return
def setTextAnnotation() -> ...: ...  # TODO need to fill in return
def setTextColor() -> ...: ...  # TODO need to fill in return
def setTextDirection() -> ...: ...  # TODO need to fill in return
def setTextDistances() -> ...: ...  # TODO need to fill in return
def textFlowMode() -> ...: ...  # TODO need to fill in return
def setTextScalingH() -> ...: ...  # TODO need to fill in return
def setTextScalingV() -> ...: ...  # TODO need to fill in return
def setTextShade() -> ...: ...  # TODO need to fill in return
def setTextStroke() -> ...: ...  # TODO need to fill in return
def setTextVerticalAlignment() -> ...: ...  # TODO need to fill in return
def setTracking() -> ...: ...  # TODO need to fill in return
def setURIAnnotation() -> ...: ...  # TODO need to fill in return
def setUnit() -> ...: ...  # TODO need to fill in return
def setVGuides() -> ...: ...  # TODO need to fill in return
def setWordTracking() -> ...: ...  # TODO need to fill in return
def sizeObject() -> ...: ...  # TODO need to fill in return
def stringValueToPoints() -> ...: ...  # TODO need to fill in return
def textOverflows() -> ...: ...  # TODO need to fill in return
def unGroupObjects() -> ...: ...  # TODO need to fill in return
def unlinkTextFrames() -> ...: ...  # TODO need to fill in return
def valueDialog() -> ...: ...  # TODO need to fill in return
def zoomDocument(double: float) -> ...: ...  # TODO need to fill in return
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
