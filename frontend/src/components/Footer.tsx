import React from 'react';
import styled from '@emotion/styled';

const FooterContainer = styled.footer`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  margin-top: 2rem;
  border-top: 1px solid #d3d6da;
  color: #787c7e;
  font-size: 0.9rem;
`;

const Link = styled.a`
  color: #538d4e;
  text-decoration: none;
  margin: 0 0.5rem;
  &:hover {
    text-decoration: underline;
  }
`;

const Footer: React.FC = () => (
    <FooterContainer>
        <span>Inspired by </span>
        <Link href="https://www.nytimes.com/games/wordle" target="_blank" rel="noopener noreferrer">
            NYT Wordle
        </Link>
        <span> • Built with AI assistance</span>
    </FooterContainer>
);

export default Footer; 