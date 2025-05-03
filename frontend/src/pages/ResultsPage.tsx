import React from 'react';
import styled from '@emotion/styled';
import NavBar from '../components/NavBar';
import PDFViewer from '../components/PDFViewer';

const Container = styled.div`
    max-width: 900px;
    margin: 60px auto 0;
    padding: 2rem 1rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
`;

const ResultsPage: React.FC = () => {
    return (
        <>
            <NavBar />
            <Container>
                <PDFViewer file="/research.pdf" />
            </Container>
        </>
    );
};

export default ResultsPage; 