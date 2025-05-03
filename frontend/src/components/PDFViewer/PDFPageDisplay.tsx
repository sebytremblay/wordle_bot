import React from 'react';
import { Page } from 'react-pdf';

interface PDFPageDisplayProps {
    pageNumber: number;
    containerWidth: number;
}

const PDFPageDisplay: React.FC<PDFPageDisplayProps> = ({ pageNumber, containerWidth }) => (
    <Page pageNumber={pageNumber} width={containerWidth} />
);

export default PDFPageDisplay; 