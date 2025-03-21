import React from 'react';
import styled from 'styled-components';

const HeaderContainer = styled.header`
    display: flex;
    justify-content: center;
    align-items: center;
    height: 65px;
    border-bottom: 1px solid #d3d6da;
    margin-bottom: 20px;
`;

const Title = styled.h1`
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: 0.2rem;
    color: #1a1a1b;
`;

const Subtitle = styled.div`
    text-align: center;
    color: #787c7e;
    font-size: 0.9rem;
    margin-top: 5px;
`;

const Header: React.FC = () => {
    return (
        <>
            <HeaderContainer>
                <Title>WORDLE SOLVER</Title>
            </HeaderContainer>
            <Subtitle>
                Play Wordle with AI assistance - Choose a solver and get hints!
            </Subtitle>
        </>
    );
};

export default Header; 