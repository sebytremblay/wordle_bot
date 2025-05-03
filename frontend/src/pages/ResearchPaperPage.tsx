import React, { useState } from 'react';
import styled from '@emotion/styled';
import { Document, Page, pdfjs } from 'react-pdf';
import NavBar from '../components/NavBar';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import { Button } from '@/styles/components/GuessInput.styles';

// Configure PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

const Container = styled.div`
    max-width: 900px;
    margin: 60px auto 0;
    padding: 2rem 1rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
`;

const Title = styled.h1`
    text-align: center;
    color: #1a1a1b;
    margin-bottom: 2rem;
`;

const PDFViewer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 700px;
`;

const Controls = styled.div`
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1rem;
`;

const PageInfo = styled.div`
    display: flex;
    justify-content: center;
    margin-top: 0.25rem;
    padding-bottom: 2rem;
    color: #787c7e;
`;

const StyledPage = styled.div`
    box-shadow: 0 2px 8px rgba(0,0,0,0.10);
    margin-bottom: 1rem;
    background: #f9f9f9;
    border-radius: 4px;
    overflow: hidden;
`;

const ResearchPaperPage: React.FC = () => {
    const [numPages, setNumPages] = useState<number | null>(null);
    const [pageNumber, setPageNumber] = useState(1);

    const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
        setNumPages(numPages);
        setPageNumber(1);
    };

    const goToPrevPage = () => setPageNumber((prev) => Math.max(prev - 1, 1));
    const goToNextPage = () => setPageNumber((prev) => (numPages ? Math.min(prev + 1, numPages) : prev));

    return (
        <>
            <NavBar />
            <Container>
                <Title>Research Paper</Title>
                <PDFViewer>
                    <StyledPage style={{ width: 800, maxWidth: '100%' }}>
                        <Document
                            file="/research.pdf"
                            onLoadSuccess={onDocumentLoadSuccess}
                            loading={<div>Loading PDF...</div>}
                            error={<div>Failed to load PDF.</div>}
                        >
                            <Page pageNumber={pageNumber} width={800} />
                        </Document>
                    </StyledPage>
                </PDFViewer>
                <PageInfo>
                    Page {pageNumber} {numPages ? `of ${numPages}` : ''}
                </PageInfo>
                <Controls>
                    <Button onClick={goToPrevPage} disabled={pageNumber <= 1}>
                        Previous
                    </Button>
                    <Button onClick={goToNextPage} disabled={numPages ? pageNumber >= numPages : true}>
                        Next
                    </Button>
                </Controls>

            </Container>
        </>
    );
};

export default ResearchPaperPage; 