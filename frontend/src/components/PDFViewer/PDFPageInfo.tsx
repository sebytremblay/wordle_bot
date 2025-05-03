import React from 'react';
import { PageInfo } from '@/styles/components/PDFViewer.styles';

interface PDFPageInfoProps {
    pageNumber: number;
    numPages: number | null;
}

const PDFPageInfo: React.FC<PDFPageInfoProps> = ({ pageNumber, numPages }) => (
    <PageInfo>
        Page {pageNumber} {numPages ? `of ${numPages}` : ''}
    </PageInfo>
);

export default PDFPageInfo; 