## This is a list of XPATHS used and maintained by The ARTFL Project
## If you add any new XPATHS, be careful to remove any trailing slash
## at the end of your XPATH otherwise LXML won't find it.

xpaths =  [("doc","."),("div",".//div"), ("div",".//div1"),("div",".//div2"),("div",".//div3"),("para",".//sp"),("page",".//pb")]

metadata_xpaths = [
                
                ## DOC LEVEL XPATHS
                
                ## Author
                ("doc", ".//sourceDesc/bibl/author[@type='marc100']", "author"),
                ("doc", ".//sourceDesc/bibl/author[@type='artfl']", "author"),
                ("doc", ".//sourceDesc/bibl/author", "author"),
                ("doc", ".//titleStmt/author", "author"),
                ("doc", ".//sourceDesc/biblStruct/monogr/author/name", "author"),
                ("doc", ".//sourceDesc/biblFull/titleStmt/author", "author"),
                ("doc", ".//sourceDesc/biblFull/titleStmt/respStmt/name", "author"),
                ("doc", ".//sourceDesc/biblFull/titleStmt/author", "author"),
                ("doc", ".//sourceDesc/bibl/titleStmt/author", "author"),
                
                ## Title XPATHs
                ("doc", ".//sourceDesc/bibl/title[@type='artfl']", "title"),
                ("doc", ".//sourceDesc/bibl/title", "title"),
                ("doc", ".//titleStmt/title", "title"),
                ("doc", ".//sourceDesc/bibl/titleStmt/title", "title"),
                ("doc", ".//sourceDesc/biblStruct/monogr/title", "title"),
                ("doc", ".//sourceDesc/biblFull/titleStmt/title", "title"),
                
                ## Author dates
                ("doc", ".//sourceDesc/bibl/author/date", "author_dates"),
                ("doc", ".//titlestmt/author/date", "author_dates"),
                
                # Date
                ("doc", ".//profileDesc/creation/date", "date"),
                ("doc", ".//fileDesc/sourceDesc/bibl/imprint/date", "date"),
                ("doc", ".//sourceDesc/biblFull/publicationStmt/date", "date"),
                ("doc", ".//sourceDesc/bibl/imprint/date", "date"),
                ("doc", ".//sourceDesc/biblFull/publicationStmt/date", "date"),
                ("doc", ".//profileDesc/dummy/creation/date", "date"),
                
                # Publisher
                ("doc", ".//sourceDesc/bibl/imprint[@type='marc534']", "publisher"),
                ("doc", ".//sourceDesc/bibl/imprint[@type='artfl']", "publisher"),
                ("doc", ".//sourceDesc/bibl/imprint/publisher", "publisher"),
                ("doc", ".//sourceDesc/biblstruct/monogr/imprint/publisher/name", "publisher"),
                ("doc", ".//sourceDesc/biblfull/publicationstmt/publisher", "publisher"),
                ("doc", ".//sourceDesc/bibl/publicationstmt/publisher", "publisher"),
                ("doc", ".//sourceDesc/bibl/publisher", "publisher"),
                ("doc", ".//publicationstmt/publisher", "publisher"),
                
                ## pub_place
                ("doc", ".//sourceDesc/bibl/imprint/pubPlace", "pub_place"),
                ("doc", ".//sourceDesc/biblFull/publicationStmt/pubPlace", "pub_place"),
                ("doc", ".//sourceDesc/biblStruct/monog/imprint/pubPlace", "pub_place"),
                ("doc", ".//sourceDesc/bibl/pubPlace", "pub_place"),
                ("doc", ".//sourceDesc/bibl/publicationStmt/pubPlace", "pub_place"),
                
                ## pub_date
                ("doc", ".//sourceDesc/bibl/imprint/date", "pub_date"),
                ("doc", ".//sourceDesc/biblStruct/monog/imprint/date", "pub_date"),
                ("doc", ".//sourceDesc/biblFull/publicationStmt/date", "pub_date"),
                ("doc", ".//sourceDesc/bibFulll/imprint/date", "pub_date"),
                ("doc", ".//sourceDesc/bibl/date", "pub_date"),
                
                ## extent
                ("doc", ".//sourceDesc/bibl/extent", "extent"),
                ("doc", ".//sourceDesc/biblStruct/monog//extent", "extent"),
                ("doc", ".//sourceDesc/biblFull/extent", "extent"),
                
                ## editor
                ("doc", ".//sourceDesc/bibl/editor", "editor"),
                ("doc", ".//sourceDesc/biblFull/titleStmt/editor", "editor"),
                ("doc", ".//sourceDesc/bibl/title/Stmt/editor", "editor"),
                
                ## identifiers
                ("doc", ".//publicationStmt/idno", "identifiers"),
                
                ## text_genre
                ("doc", ".//profileDesc/textClass/keywords[@scheme='genre']/term", "text_genre"),
                
                ## keywords
                ("doc", ".//profileDesc/textClass/keywords/list/item", "keywords"),
                
                ## language
                ("doc", ".//profileDesc/langusage/language", "language"),
                
                ## notes
                ("doc", ".//fileDesc/notesStmt/note", "notes"),
                ("doc", ".//publicationStmt/notesStmt/note", "notes"),
                
                ## auth_gender
                ("doc", ".//publicationStmt/notesStmt/note", "auth_gender"),
                
                ## collection
                ("doc", ".//seriesStmt/title", "collection"),
                
                ## period
                ("doc", ".//profileDesc/textClass/keywords[@scheme='period']/list/item", "period"),
                
                #text_form
                ("doc", ".//profileDesc/textClass/keywords[@scheme='form']/term", "text_form"),
                
                ## DIV LEVEL XPATHS
                ("div","./head","head"),
                ("div",".@n","n"),
                ("div",".@id","id"),
                
                ## PARAGRAPH LEVEL XPATHS
                ("para", ".@who", "who"),
                
                ## PAGE LEVEL XPATHS
                ("page",".@n","n"),
                ("page",".@fac","img")
                ]