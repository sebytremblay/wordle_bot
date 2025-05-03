import React, { useState } from 'react';
import { Document, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import { ViewerContainer, StyledPage } from '../styles/components/PDFViewer.styles';
import PDFViewerControls from './PDFViewer/PDFViewerControls';
import PDFPageDisplay from './PDFViewer/PDFPageDisplay';
import PDFPageInfo from './PDFViewer/PDFPageInfo';

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

export interface PDFViewerProps {
    file: string;
    initialPage?: number;
    containerWidth?: number;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ file, initialPage = 1, containerWidth = 800 }) => {
    const [numPages, setNumPages] = useState<number | null>(null);
    const [pageNumber, setPageNumber] = useState(initialPage);

    const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
        setNumPages(numPages);
        setPageNumber(1);
    };

    const goToPrevPage = () => setPageNumber((prev) => Math.max(prev - 1, 1));
    const goToNextPage = () => setPageNumber((prev) => (numPages ? Math.min(prev + 1, numPages) : prev));

    return (
        <ViewerContainer>
            <StyledPage width={containerWidth}>
                <Document
                    file={file}
                    onLoadSuccess={onDocumentLoadSuccess}
                    loading={<div>Loading PDF...</div>}
                    error={<div>Failed to load PDF.</div>}
                >
                    <PDFPageDisplay pageNumber={pageNumber} containerWidth={containerWidth} />
                </Document>
            </StyledPage>
            <PDFPageInfo pageNumber={pageNumber} numPages={numPages} />
            <PDFViewerControls
                pageNumber={pageNumber}
                numPages={numPages}
                goToPrevPage={goToPrevPage}
                goToNextPage={goToNextPage}
            />
        </ViewerContainer>
    );
};

export default PDFViewer; 