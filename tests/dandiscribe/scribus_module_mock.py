from unittest import mock


class ScribusSpec:
    __name__ = "scribus"
    __doc__ = ""
    __package__ = ""
    applyMasterPage = mock.Mock(name="scribus.applyMasterPage")
    changeColor = mock.Mock(name="scribus.changeColor")
    changeColorCMYK = mock.Mock(name="scribus.changeColorCMYK")
    changeColorCMYKFloat = mock.Mock(name="scribus.changeColorCMYKFloat")
    changeColorLab = mock.Mock(name="scribus.changeColorLab")
    changeColorRGB = mock.Mock(name="scribus.changeColorRGB")
    changeColorRGBFloat = mock.Mock(name="scribus.changeColorRGBFloat")
    closeDoc = mock.Mock(name="scribus.closeDoc")
    closeMasterPage = mock.Mock(name="scribus.closeMasterPage")
    createBezierLine = mock.Mock(name="scribus.createBezierLine")
    createCharStyle = mock.Mock(name="scribus.createCharStyle")
    createCustomLineStyle = mock.Mock(name="scribus.createCustomLineStyle")
    createEllipse = mock.Mock(name="scribus.createEllipse")
    createImage = mock.Mock(name="scribus.createImage")
    createLayer = mock.Mock(name="scribus.createLayer")
    createLine = mock.Mock(name="scribus.createLine")
    createMasterPage = mock.Mock(name="scribus.createMasterPage")
    createParagraphStyle = mock.Mock(name="scribus.createParagraphStyle")
    createPathText = mock.Mock(name="scribus.createPathText")
    createPolyLine = mock.Mock(name="scribus.createPolyLine")
    createPolygon = mock.Mock(name="scribus.createPolygon")
    createRect = mock.Mock(name="scribus.createRect")
    createTable = mock.Mock(name="scribus.createTable")
    createText = mock.Mock(name="scribus.createText")
    currentPage = mock.Mock(name="scribus.currentPage")
    currentPageNumber = mock.Mock(name="scribus.currentPageNumber")
    currentPageNumberForSection = mock.Mock(
        name="scribus.currentPageNumberForSection"
    )
    defineColor = mock.Mock(name="scribus.defineColor")
    defineColorCMYK = mock.Mock(name="scribus.defineColorCMYK")
    defineColorCMYKFloat = mock.Mock(name="scribus.defineColorCMYKFloat")
    defineColorLab = mock.Mock(name="scribus.defineColorLab")
    defineColorRGB = mock.Mock(name="scribus.defineColorRGB")
    defineColorRGBFloat = mock.Mock(name="scribus.defineColorRGBFloat")
    dehyphenateText = mock.Mock(name="scribus.dehyphenateText")
    deleteColor = mock.Mock(name="scribus.deleteColor")
    deleteLayer = mock.Mock(name="scribus.deleteLayer")
    deleteMasterPage = mock.Mock(name="scribus.deleteMasterPage")
    deleteObject = mock.Mock(name="scribus.deleteObject")
    deletePage = mock.Mock(name="scribus.deletePage")
    deleteText = mock.Mock(name="scribus.deleteText")
    deselectAll = mock.Mock(name="scribus.deselectAll")
    docChanged = mock.Mock(name="scribus.docChanged")
    editMasterPage = mock.Mock(name="scribus.editMasterPage")
    fileDialog = mock.Mock(name="scribus.fileDialog")
    fileQuit = mock.Mock(name="scribus.fileQuit")
    flipObject = mock.Mock(name="scribus.flipObject")
    getActiveLayer = mock.Mock(name="scribus.getActiveLayer")
    getAllObjects = mock.Mock(name="scribus.getAllObjects")
    getAllStyles = mock.Mock(name="scribus.getAllStyles")
    getAllText = mock.Mock(name="scribus.getAllText")
    getBaseLine = mock.Mock(name="scribus.getBaseLine")
    getBleeds = mock.Mock(name="scribus.getBleeds")
    getCellColumnSpan = mock.Mock(name="scribus.getCellColumnSpan")
    getCellFillColor = mock.Mock(name="scribus.getCellFillColor")
    getCellRowSpan = mock.Mock(name="scribus.getCellRowSpan")
    getCellStyle = mock.Mock(name="scribus.getCellStyle")
    getCellStyles = mock.Mock(name="scribus.getCellStyles")
    getCellText = mock.Mock(name="scribus.getCellText")
    getCharStyles = mock.Mock(name="scribus.getCharStyles")
    getCharacterStyle = mock.Mock(name="scribus.getCharacterStyle")
    getColor = mock.Mock(name="scribus.getColor")
    getColorAsRGB = mock.Mock(name="scribus.getColorAsRGB")
    getColorAsRGBFloat = mock.Mock(name="scribus.getColorAsRGBFloat")
    getColorFloat = mock.Mock(name="scribus.getColorFloat")
    getColorNames = mock.Mock(name="scribus.getColorNames")
    getColumnGap = mock.Mock(name="scribus.getColumnGap")
    getColumns = mock.Mock(name="scribus.getColumns")
    getColumnGuides = mock.Mock(name="scribus.getColumnGuides")
    getCornerRadius = mock.Mock(name="scribus.getCornerRadius")
    getCustomLineStyle = mock.Mock(name="scribus.getCustomLineStyle")
    getDocName = mock.Mock(name="scribus.getDocName")
    getFillBlendmode = mock.Mock(name="scribus.getFillBlendmode")
    getFillColor = mock.Mock(name="scribus.getFillColor")
    getFillShade = mock.Mock(name="scribus.getFillShade")
    getFillTransparency = mock.Mock(name="scribus.getFillTransparency")
    getFirstLineOffset = mock.Mock(name="scribus.getFirstLineOffset")
    getFirstLinkedFrame = mock.Mock(name="scribus.getFirstLinkedFrame")
    getFont = mock.Mock(name="scribus.getFont")
    getFontFeatures = mock.Mock(name="scribus.getFontFeatures")
    getFontNames = mock.Mock(name="scribus.getFontNames")
    getFontSize = mock.Mock(name="scribus.getFontSize")
    getFrameText = mock.Mock(name="scribus.getFrameText")
    getFrameSelectedTextRange = mock.Mock(
        name="scribus.getFrameSelectedTextRange"
    )
    getGroupItems = mock.Mock(name="scribus.getGroupItems")
    getGuiLanguage = mock.Mock(name="scribus.getGuiLanguage")
    getHGuides = mock.Mock(name="scribus.getHGuides")
    getImageColorSpace = mock.Mock(name="scribus.getImageColorSpace")
    getImageFile = mock.Mock(name="scribus.getImageFile")
    getImageOffset = mock.Mock(name="scribus.getImageOffset")
    getImageScale = mock.Mock(name="scribus.getImageScale")
    getInfo = mock.Mock(name="scribus.getInfo")
    getItemPageNumber = mock.Mock(name="scribus.getItemPageNumber")
    getLastLinkedFrame = mock.Mock(name="scribus.getLastLinkedFrame")
    getLayerBlendmode = mock.Mock(name="scribus.getLayerBlendmode")
    getLayerTransparency = mock.Mock(name="scribus.getLayerTransparency")
    getLayers = mock.Mock(name="scribus.getLayers")
    getLineBlendmode = mock.Mock(name="scribus.getLineBlendmode")
    getLineCap = mock.Mock(name="scribus.getLineCap")
    getLineColor = mock.Mock(name="scribus.getLineColor")
    getLineJoin = mock.Mock(name="scribus.getLineJoin")
    getLineShade = mock.Mock(name="scribus.getLineShade")
    getLineSpacing = mock.Mock(name="scribus.getLineSpacing")
    getLineSpacingMode = mock.Mock(name="scribus.getLineSpacingMode")
    getLineStyle = mock.Mock(name="scribus.getLineStyle")
    getLineStyles = mock.Mock(name="scribus.getLineStyles")
    getLineTransparency = mock.Mock(name="scribus.getLineTransparency")
    getLineWidth = mock.Mock(name="scribus.getLineWidth")
    getMargins = mock.Mock(name="scribus.getMargins")
    getMasterPage = mock.Mock(name="scribus.getMasterPage")
    getNextLinkedFrame = mock.Mock(name="scribus.getNextLinkedFrame")
    getObjectAttributes = mock.Mock(name="scribus.getObjectAttributes")
    getObjectType = mock.Mock(name="scribus.getObjectType")
    getPageItems = mock.Mock(name="scribus.getPageItems")
    getPageMargins = mock.Mock(name="scribus.getPageMargins")
    getPageNMargins = mock.Mock(name="scribus.getPageNMargins")
    getPageNSize = mock.Mock(name="scribus.getPageNSize")
    getPageSize = mock.Mock(name="scribus.getPageSize")
    getPageType = mock.Mock(name="scribus.getPageType")
    getParagraphStyle = mock.Mock(name="scribus.getParagraphStyle")
    getParagraphStyles = mock.Mock(name="scribus.getParagraphStyles")
    getPosition = mock.Mock(name="scribus.getPosition")
    getPrevLinkedFrame = mock.Mock(name="scribus.getPrevLinkedFrame")
    getRotation = mock.Mock(name="scribus.getRotation")
    getRowGuides = mock.Mock(name="scribus.getRowGuides")
    getSelectedObject = mock.Mock(name="scribus.getSelectedObject")
    getSelectedTextRange = mock.Mock(name="scribus.getSelectedTextRange")
    getSize = mock.Mock(name="scribus.getSize")
    getStyle = mock.Mock(name="scribus.getStyle")
    getTableColumnWidth = mock.Mock(name="scribus.getTableColumnWidth")
    getTableColumns = mock.Mock(name="scribus.getTableColumns")
    getTableFillColor = mock.Mock(name="scribus.getTableFillColor")
    getTableRowHeight = mock.Mock(name="scribus.getTableRowHeight")
    getTableRows = mock.Mock(name="scribus.getTableRows")
    getTableStyle = mock.Mock(name="scribus.getTableStyle")
    getTableStyles = mock.Mock(name="scribus.getTableStyles")
    getText = mock.Mock(name="scribus.getText")
    getTextColor = mock.Mock(name="scribus.getTextColor")
    getTextDistances = mock.Mock(name="scribus.getTextDistances")
    getTextFlowMode = mock.Mock(name="scribus.getTextFlowMode")
    getTextLength = mock.Mock(name="scribus.getTextLength")
    getTextLines = mock.Mock(name="scribus.getTextLines")
    getTextShade = mock.Mock(name="scribus.getTextShade")
    getTextVerticalAlignment = mock.Mock(
        name="scribus.getTextVerticalAlignment"
    )
    getUnit = mock.Mock(name="scribus.getUnit")
    pointsToDocUnit = mock.Mock(name="scribus.pointsToDocUnit")
    docUnitToPoints = mock.Mock(name="scribus.docUnitToPoints")
    stringValueToPoints = mock.Mock(name="scribus.stringValueToPoints")
    getVGuides = mock.Mock(name="scribus.getVGuides")
    getXFontNames = mock.Mock(name="scribus.getXFontNames")
    gotoPage = mock.Mock(name="scribus.gotoPage")
    groupObjects = mock.Mock(name="scribus.groupObjects")
    haveDoc = mock.Mock(name="scribus.haveDoc")
    hyphenateText = mock.Mock(name="scribus.hyphenateText")
    importPage = mock.Mock(name="scribus.importPage")
    insertHtmlText = mock.Mock(name="scribus.insertHtmlText")
    insertTableColumns = mock.Mock(name="scribus.insertTableColumns")
    insertTableRows = mock.Mock(name="scribus.insertTableRows")
    insertText = mock.Mock(name="scribus.insertText")
    isLayerFlow = mock.Mock(name="scribus.isLayerFlow")
    isLayerLocked = mock.Mock(name="scribus.isLayerLocked")
    isLayerOutlined = mock.Mock(name="scribus.isLayerOutlined")
    isLayerPrintable = mock.Mock(name="scribus.isLayerPrintable")
    isLayerVisible = mock.Mock(name="scribus.isLayerVisible")
    isLocked = mock.Mock(name="scribus.isLocked")
    isPDFBookmark = mock.Mock(name="scribus.isPDFBookmark")
    isSpotColor = mock.Mock(name="scribus.isSpotColor")
    layoutText = mock.Mock(name="scribus.layoutText")
    layoutTextChain = mock.Mock(name="scribus.layoutTextChain")
    linkTextFrames = mock.Mock(name="scribus.linkTextFrames")
    loadImage = mock.Mock(name="scribus.loadImage")
    loadStylesFromFile = mock.Mock(name="scribus.loadStylesFromFile")
    lockObject = mock.Mock(name="scribus.lockObject")
    lowerActiveLayer = mock.Mock(name="scribus.lowerActiveLayer")
    masterPageNames = mock.Mock(name="scribus.masterPageNames")
    mergeTableCells = mock.Mock(name="scribus.mergeTableCells")
    messageBox = mock.Mock(name="scribus.messageBox")
    messagebarText = mock.Mock(name="scribus.messagebarText")
    moveObject = mock.Mock(name="scribus.moveObject")
    moveObjectAbs = mock.Mock(name="scribus.moveObjectAbs")
    moveSelectionToBack = mock.Mock(name="scribus.moveSelectionToBack")
    moveSelectionToFront = mock.Mock(name="scribus.moveSelectionToFront")
    newDoc = mock.Mock(name="scribus.newDoc")
    newDocDialog = mock.Mock(name="scribus.newDocDialog")
    newDocument = mock.Mock(name="scribus.newDocument")
    newPage = mock.Mock(name="scribus.newPage")
    newStyleDialog = mock.Mock(name="scribus.newStyleDialog")
    objectExists = mock.Mock(name="scribus.objectExists")
    openDoc = mock.Mock(name="scribus.openDoc")
    outlineText = mock.Mock(name="scribus.outlineText")
    pageCount = mock.Mock(name="scribus.pageCount")
    pageDimension = mock.Mock(name="scribus.pageDimension")
    placeEPS = mock.Mock(name="scribus.placeEPS")
    placeODG = mock.Mock(name="scribus.placeODG")
    placeSVG = mock.Mock(name="scribus.placeSVG")
    placeSXD = mock.Mock(name="scribus.placeSXD")
    placeVectorFile = mock.Mock(name="scribus.placeVectorFile")
    progressReset = mock.Mock(name="scribus.progressReset")
    progressSet = mock.Mock(name="scribus.progressSet")
    progressTotal = mock.Mock(name="scribus.progressTotal")
    raiseActiveLayer = mock.Mock(name="scribus.raiseActiveLayer")
    readPDFOptions = mock.Mock(name="scribus.readPDFOptions")
    redrawAll = mock.Mock(name="scribus.redrawAll")
    removeTableColumns = mock.Mock(name="scribus.removeTableColumns")
    removeTableRows = mock.Mock(name="scribus.removeTableRows")
    renderFont = mock.Mock(name="scribus.renderFont")
    replaceColor = mock.Mock(name="scribus.replaceColor")
    resizeTableColumn = mock.Mock(name="scribus.resizeTableColumn")
    resizeTableRow = mock.Mock(name="scribus.resizeTableRow")
    revertDoc = mock.Mock(name="scribus.revertDoc")
    rotateObject = mock.Mock(name="scribus.rotateObject")
    rotateObjectAbs = mock.Mock(name="scribus.rotateObjectAbs")
    saveDoc = mock.Mock(name="scribus.saveDoc")
    saveDocAs = mock.Mock(name="scribus.saveDocAs")
    savePDFOptions = mock.Mock(name="scribus.savePDFOptions")
    savePageAsEPS = mock.Mock(name="scribus.savePageAsEPS")
    scaleGroup = mock.Mock(name="scribus.scaleGroup")
    scaleImage = mock.Mock(name="scribus.scaleImage")
    scrollDocument = mock.Mock(name="scribus.scrollDocument")
    selectFrameText = mock.Mock(name="scribus.selectFrameText")
    selectObject = mock.Mock(name="scribus.selectObject")
    selectText = mock.Mock(name="scribus.selectText")
    selectionCount = mock.Mock(name="scribus.selectionCount")
    sendToLayer = mock.Mock(name="scribus.sendToLayer")
    sentToLayer = mock.Mock(name="scribus.sentToLayer")
    setActiveLayer = mock.Mock(name="scribus.setActiveLayer")
    setBaseLine = mock.Mock(name="scribus.setBaseLine")
    setBleeds = mock.Mock(name="scribus.setBleeds")
    setCellBottomBorder = mock.Mock(name="scribus.setCellBottomBorder")
    setCellBottomPadding = mock.Mock(name="scribus.setCellBottomPadding")
    setCellFillColor = mock.Mock(name="scribus.setCellFillColor")
    setCellLeftBorder = mock.Mock(name="scribus.setCellLeftBorder")
    setCellLeftPadding = mock.Mock(name="scribus.setCellLeftPadding")
    setCellRightBorder = mock.Mock(name="scribus.setCellRightBorder")
    setCellRightPadding = mock.Mock(name="scribus.setCellRightPadding")
    setCellStyle = mock.Mock(name="scribus.setCellStyle")
    setCellText = mock.Mock(name="scribus.setCellText")
    setCellTopBorder = mock.Mock(name="scribus.setCellTopBorder")
    setCellTopPadding = mock.Mock(name="scribus.setCellTopPadding")
    setCharacterStyle = mock.Mock(name="scribus.setCharacterStyle")
    setColumnGap = mock.Mock(name="scribus.setColumnGap")
    setColumns = mock.Mock(name="scribus.setColumns")
    setColumnGuides = mock.Mock(name="scribus.setColumnGuides")
    setCornerRadius = mock.Mock(name="scribus.setCornerRadius")
    setCursor = mock.Mock(name="scribus.setCursor")
    setCustomLineStyle = mock.Mock(name="scribus.setCustomLineStyle")
    setDocType = mock.Mock(name="scribus.setDocType")
    setEditMode = mock.Mock(name="scribus.setEditMode")
    setFillBlendmode = mock.Mock(name="scribus.setFillBlendmode")
    setFillColor = mock.Mock(name="scribus.setFillColor")
    setFillShade = mock.Mock(name="scribus.setFillShade")
    setFillTransparency = mock.Mock(name="scribus.setFillTransparency")
    setFirstLineOffset = mock.Mock(name="scribus.setFirstLineOffset")
    setFont = mock.Mock(name="scribus.setFont")
    setFontFeatures = mock.Mock(name="scribus.setFontFeatures")
    setFontSize = mock.Mock(name="scribus.setFontSize")
    setGradientFill = mock.Mock(name="scribus.setGradientFill")
    setGradientStop = mock.Mock(name="scribus.setGradientStop")
    setHGuides = mock.Mock(name="scribus.setHGuides")
    setImageBrightness = mock.Mock(name="scribus.setImageBrightness")
    setImageGrayscale = mock.Mock(name="scribus.setImageGrayscale")
    setImageOffset = mock.Mock(name="scribus.setImageOffset")
    setImageScale = mock.Mock(name="scribus.setImageScale")
    setInfo = mock.Mock(name="scribus.setInfo")
    setItemName = mock.Mock(name="scribus.setItemName")
    setNormalMode = mock.Mock(name="scribus.setNormalMode")
    setLayerBlendmode = mock.Mock(name="scribus.setLayerBlendmode")
    setLayerFlow = mock.Mock(name="scribus.setLayerFlow")
    setLayerLocked = mock.Mock(name="scribus.setLayerLocked")
    setLayerOutlined = mock.Mock(name="scribus.setLayerOutlined")
    setLayerPrintable = mock.Mock(name="scribus.setLayerPrintable")
    setLayerTransparency = mock.Mock(name="scribus.setLayerTransparency")
    setLayerVisible = mock.Mock(name="scribus.setLayerVisible")
    setLineBlendmode = mock.Mock(name="scribus.setLineBlendmode")
    setLineCap = mock.Mock(name="scribus.setLineCap")
    setLineColor = mock.Mock(name="scribus.setLineColor")
    setLineJoin = mock.Mock(name="scribus.setLineJoin")
    setLineShade = mock.Mock(name="scribus.setLineShade")
    setLineSpacing = mock.Mock(name="scribus.setLineSpacing")
    setLineSpacingMode = mock.Mock(name="scribus.setLineSpacingMode")
    setLineStyle = mock.Mock(name="scribus.setLineStyle")
    setLineTransparency = mock.Mock(name="scribus.setLineTransparency")
    setLineWidth = mock.Mock(name="scribus.setLineWidth")
    setMargins = mock.Mock(name="scribus.setMargins")
    setMultiLine = mock.Mock(name="scribus.setMultiLine")
    setNewName = mock.Mock(name="scribus.setNewName")
    setObjectAttributes = mock.Mock(name="scribus.setObjectAttributes")
    setPDFBookmark = mock.Mock(name="scribus.setPDFBookmark")
    setParagraphStyle = mock.Mock(name="scribus.setParagraphStyle")
    setRedraw = mock.Mock(name="scribus.setRedraw")
    setRotation = mock.Mock(name="scribus.setRotation")
    setRowGuides = mock.Mock(name="scribus.setRowGuides")
    setScaleFrameToImage = mock.Mock(name="scribus.setScaleFrameToImage")
    setScaleImageToFrame = mock.Mock(name="scribus.setScaleImageToFrame")
    setSpotColor = mock.Mock(name="scribus.setSpotColor")
    setStyle = mock.Mock(name="scribus.setStyle")
    setTableBottomBorder = mock.Mock(name="scribus.setTableBottomBorder")
    setTableFillColor = mock.Mock(name="scribus.setTableFillColor")
    setTableLeftBorder = mock.Mock(name="scribus.setTableLeftBorder")
    setTableRightBorder = mock.Mock(name="scribus.setTableRightBorder")
    setTableStyle = mock.Mock(name="scribus.setTableStyle")
    setTableTopBorder = mock.Mock(name="scribus.setTableTopBorder")
    setText = mock.Mock(name="scribus.setText")
    setTextAlignment = mock.Mock(name="scribus.setTextAlignment")
    setTextColor = mock.Mock(name="scribus.setTextColor")
    setTextDirection = mock.Mock(name="scribus.setTextDirection")
    setTextDistances = mock.Mock(name="scribus.setTextDistances")
    setTextFlowMode = mock.Mock(name="scribus.setTextFlowMode")
    setTextScalingH = mock.Mock(name="scribus.setTextScalingH")
    setTextScalingV = mock.Mock(name="scribus.setTextScalingV")
    setTextShade = mock.Mock(name="scribus.setTextShade")
    setTextStroke = mock.Mock(name="scribus.setTextStroke")
    setTextVerticalAlignment = mock.Mock(
        name="scribus.setTextVerticalAlignment"
    )
    setUnit = mock.Mock(name="scribus.setUnit")
    setVGuides = mock.Mock(name="scribus.setVGuides")
    sizeObject = mock.Mock(name="scribus.sizeObject")
    statusMessage = mock.Mock(name="scribus.statusMessage")
    textFlowMode = mock.Mock(name="scribus.textFlowMode")
    textOverflows = mock.Mock(name="scribus.textOverflows")
    traceText = mock.Mock(name="scribus.traceText")
    unGroupObject = mock.Mock(name="scribus.unGroupObject")
    unGroupObjects = mock.Mock(name="scribus.unGroupObjects")
    unlinkTextFrames = mock.Mock(name="scribus.unlinkTextFrames")
    valueDialog = mock.Mock(name="scribus.valueDialog")
    zoomDocument = mock.Mock(name="scribus.zoomDocument")
    getPropertyCType = mock.Mock(name="scribus.getPropertyCType")
    getPropertyNames = mock.Mock(name="scribus.getPropertyNames")
    getProperty = mock.Mock(name="scribus.getProperty")
    setProperty = mock.Mock(name="scribus.setProperty")
    copyObject = mock.Mock(name="scribus.copyObject")
    copyObjects = mock.Mock(name="scribus.copyObjects")
    duplicateObject = mock.Mock(name="scribus.duplicateObject")
    duplicateObjects = mock.Mock(name="scribus.duplicateObjects")
    pasteObject = mock.Mock(name="scribus.pasteObject")
    pasteObjects = mock.Mock(name="scribus.pasteObjects")
    combinePolygons = mock.Mock(name="scribus.combinePolygons")
    retval = mock.Mock(name="scribus.retval")
    getval = mock.Mock(name="scribus.getval")
    setLinkAnnotation = mock.Mock(name="scribus.setLinkAnnotation")
    setFileAnnotation = mock.Mock(name="scribus.setFileAnnotation")
    setURIAnnotation = mock.Mock(name="scribus.setURIAnnotation")
    setTextAnnotation = mock.Mock(name="scribus.setTextAnnotation")
    createPdfAnnotation = mock.Mock(name="scribus.createPdfAnnotation")
    isAnnotated = mock.Mock(name="scribus.isAnnotated")
    setJSActionScript = mock.Mock(name="scribus.setJSActionScript")
    getJSActionScript = mock.Mock(name="scribus.getJSActionScript")
    Printer = mock.Mock(name="scribus.Printer")
    PDFfile = mock.Mock(name="scribus.PDFfile")
    ImageExport = mock.Mock(name="scribus.ImageExport")
    ScribusException = mock.Mock(name="scribus.ScribusException")
    NoDocOpenError = mock.Mock(name="scribus.NoDocOpenError")
    WrongFrameTypeError = mock.Mock(name="scribus.WrongFrameTypeError")
    NoValidObjectError = mock.Mock(name="scribus.NoValidObjectError")
    NotFoundError = mock.Mock(name="scribus.NotFoundError")
    NameExistsError = mock.Mock(name="scribus.NameExistsError")
    UNIT_POINTS = 0
    UNIT_MILLIMETERS = 1
    UNIT_INCHES = 2
    UNIT_PICAS = 3
    UNIT_CENTIMETRES = 4
    UNIT_CICERO = 5
    UNIT_PT = 0
    UNIT_MM = 1
    UNIT_IN = 2
    UNIT_P = 3
    UNIT_CM = 4
    UNIT_C = 5
    PORTRAIT = 0
    LANDSCAPE = 1
    NOFACINGPAGES = 0
    FACINGPAGES = 1
    FIRSTPAGERIGHT = 1
    FIRSTPAGELEFT = 0
    ALIGN_LEFT = 0
    ALIGN_RIGHT = 2
    ALIGN_CENTERED = 1
    ALIGN_BLOCK = 3
    ALIGN_FORCED = 4
    ALIGNV_TOP = 0
    ALIGNV_CENTERED = 1
    ALIGNV_BOTTOM = 2
    DIRECTION_LTR = 0
    DIRECTION_RTL = 1
    FLOP_REALGLYPHHEIGHT = 0
    FLOP_FONTASCENT = 1
    FLOP_LINESPACING = 2
    FLOP_BASELINEGRID = 3
    FILL_NOG = 0
    FILL_HORIZONTALG = 1
    FILL_VERTICALG = 2
    FILL_DIAGONALG = 3
    FILL_CROSSDIAGONALG = 4
    FILL_RADIALG = 5
    LINE_SOLID = 1
    LINE_DASH = 2
    LINE_DOT = 3
    LINE_DASHDOT = 4
    LINE_DASHDOTDOT = 5
    JOIN_MITTER = 0
    JOIN_BEVEL = 64
    JOIN_ROUND = 128
    CAP_FLAT = 0
    CAP_SQUARE = 16
    CAP_ROUND = 32
    BUTTON_NONE = 0
    BUTTON_OK = 1024
    BUTTON_CANCEL = 4194304
    BUTTON_YES = 16384
    BUTTON_NO = 65536
    BUTTON_ABORT = 262144
    BUTTON_RETRY = 524288
    BUTTON_IGNORE = 1048576
    BUTTON_DEFAULT = 256
    BUTTON_ESCAPE = 512
    ICON_NONE = 0
    ICON_INFORMATION = 1
    ICON_WARNING = 2
    ICON_CRITICAL = 3
    PAPER_A0 = (2380.0, 3368.0)
    PAPER_A1 = (1684.0, 2380.0)
    PAPER_A2 = (1190.0, 1684.0)
    PAPER_A3 = (842.0, 1190.0)
    PAPER_A4 = (595.0, 842.0)
    PAPER_A5 = (421.0, 595.0)
    PAPER_A6 = (297.0, 421.0)
    PAPER_A7 = (210.0, 297.0)
    PAPER_A8 = (148.0, 210.0)
    PAPER_A9 = (105.0, 148.0)
    PAPER_A0_MM = (841.0, 1189.0)
    PAPER_A1_MM = (594.0, 841.0)
    PAPER_A2_MM = (420.0, 594.0)
    PAPER_A3_MM = (297.0, 420.0)
    PAPER_A4_MM = (210.0, 297.0)
    PAPER_A5_MM = (148.0, 210.0)
    PAPER_A6_MM = (105.0, 148.0)
    PAPER_A7_MM = (74.0, 105.0)
    PAPER_A8_MM = (52.0, 74.0)
    PAPER_A9_MM = (37.0, 52.0)
    PAPER_B0 = (2836.0, 4008.0)
    PAPER_B1 = (2004.0, 2836.0)
    PAPER_B2 = (1418.0, 2004.0)
    PAPER_B3 = (1002.0, 1418.0)
    PAPER_B4 = (709.0, 1002.0)
    PAPER_B5 = (501.0, 709.0)
    PAPER_B6 = (355.0, 501.0)
    PAPER_B7 = (250.0, 355.0)
    PAPER_B8 = (178.0, 250.0)
    PAPER_B9 = (125.0, 178.0)
    PAPER_B10 = (89.0, 125.0)
    PAPER_B0_MM = (1000.0, 1414.0)
    PAPER_B1_MM = (707.0, 1000.0)
    PAPER_B2_MM = (500.0, 707.0)
    PAPER_B3_MM = (353.0, 500.0)
    PAPER_B4_MM = (250.0, 353.0)
    PAPER_B5_MM = (176.0, 250.0)
    PAPER_B6_MM = (125.0, 176.0)
    PAPER_B7_MM = (88.0, 125.0)
    PAPER_B8_MM = (62.0, 88.0)
    PAPER_B9_MM = (44.0, 62.0)
    PAPER_B10_MM = (31.0, 44.0)
    PAPER_C5E = (462.0, 649.0)
    PAPER_COMM10E = (298.0, 683.0)
    PAPER_DLE = (312.0, 624.0)
    PAPER_EXECUTIVE = (542.0, 720.0)
    PAPER_FOLIO = (595.0, 935.0)
    PAPER_LEDGER = (1224.0, 792.0)
    PAPER_LEGAL = (612.0, 1008.0)
    PAPER_LETTER = (612.0, 792.0)
    PAPER_TABLOID = (792.0, 1224.0)
    ITEMTYPE_ITEMTYPE1 = 1
    ITEMTYPE_IMAGEFRAME = 2
    ITEMTYPE_ITEMTYPE3 = 3
    ITEMTYPE_TEXTFRAME = 4
    ITEMTYPE_LINE = 5
    ITEMTYPE_POLYGON = 6
    ITEMTYPE_POLYLINE = 7
    ITEMTYPE_PATHTEXT = 8
    ITEMTYPE_LATEXFRAME = 9
    ITEMTYPE_OSGFRAME = 10
    ITEMTYPE_SYMBOL = 11
    ITEMTYPE_GROUP = 12
    ITEMTYPE_REGULARPOLYGON = 13
    ITEMTYPE_ARC = 14
    ITEMTYPE_SPIRAL = 15
    ITEMTYPE_TABLE = 16
    ITEMTYPE_NOTEFRAME = 17
    ITEMTYPE_MULTIPLE = 99
    CSPACE_UNDEFINED = -1
    CSPACE_RGB = 0
    CSPACE_CMYK = 1
    CSPACE_GRAY = 2
    CSPACE_DUOTONE = 3
    CSPACE_MONOCHROME = 4
    NORMAL = 0
    DARKEN = 1
    LIGHTEN = 2
    MULTIPLY = 3
    SCREEN = 4
    OVERLAY = 5
    HARD_LIGHT = 6
    SOFT_LIGHT = 7
    DIFFERENCE = 8
    EXCLUSION = 9
    COLOR_DODGE = 10
    COLOR_BURN = 11
    HUE = 12
    SATURATION = 13
    COLOR = 14
    LUMINOSITY = 15
    PAGE_1 = 0
    PAGE_2 = 1
    PAGE_3 = 2
    PAGE_4 = 3
    PRNLANG_POSTSCRIPT1 = 1
    PRNLANG_POSTSCRIPT2 = 2
    PRNLANG_POSTSCRIPT3 = 3
    PRNLANG_WINDOWSGDI = 4
    PRNLANG_PDF = 5
    TAB_LEFT = 0
    TAB_RIGHT = 1
    TAB_PERIOD = 2
    TAB_COMMA = 3
    TAB_CENTER = 4
    BASEPOINT_TOPLEFT = 1
    BASEPOINT_TOP = 2
    BASEPOINT_TOPRIGHT = 3
    BASEPOINT_LEFT = 4
    BASEPOINT_CENTER = 5
    BASEPOINT_RIGHT = 6
    BASEPOINT_BOTTOMLEFT = 7
    BASEPOINT_BOTTOM = 8
    BASEPOINT_BOTTOMRIGHT = 9
    pt = 1.0
    mm = 0.35277777777777775
    inch = 0.013888888888888888
    p = 1.0
    cm = 0.035277777777777776
    c = 0.07818656422379827
    scribus_version = "1.6.3"
    SCRIBUS_VERSION = "1.6.3"
    scribus_version_info = (1, 6, 3, "", 0)
    SCRIBUS_VERSION_INFO = (1, 6, 3, "", 0)
    builtins = mock.Mock(name="builtins")
    warnings = mock.Mock(name="warnings")
    qApp = mock.Mock(name="scribus.qApp")
    mainWindow = None
    _ia = mock.Mock(name="scribus._ia")
    _bu = mock.Mock(name="scribus._bu")
    mainInterpreter = True
