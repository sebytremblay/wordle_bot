import React from 'react';
import styled from '@emotion/styled';

const HeaderContainer = styled.header`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #d3d6da;
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  color: #1a1a1b;
  letter-spacing: 0.2rem;
`;

const Subtitle = styled.p`
  font-size: 1rem;
  color: #787c7e;
  margin: 0.5rem 0;
  text-align: center;
  max-width: 600px;
`;

const Header: React.FC = () => (
    <HeaderContainer>
        <Title>WORDLE SOLVER</Title>
        <Subtitle>
            Play Wordle with AI assistance! Enter your guesses or get hints from different solving strategies.
            The colored feedback shows how close your guess was: green for correct position, yellow for correct letter in wrong position.
        </Subtitle>
    </HeaderContainer>
);

export default Header; 