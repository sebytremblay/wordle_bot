import React from 'react';
import { Button } from '@/styles/components/GuessInput.styles';
import { Controls } from '@/styles/components/PDFViewer.styles';

interface PDFViewerControlsProps {
    pageNumber: number;
    numPages: number | null;
    goToPrevPage: () => void;
    goToNextPage: () => void;
}

const PDFViewerControls: React.FC<PDFViewerControlsProps> = ({
    pageNumber,
    numPages,
    goToPrevPage,
    goToNextPage,
}) => (
    <Controls>
        <Button onClick={goToPrevPage} disabled={pageNumber <= 1}>
            Previous
        </Button>
        <Button onClick={goToNextPage} disabled={numPages ? pageNumber >= numPages : true}>
            Next
        </Button>
    </Controls>
);

export default PDFViewerControls; 