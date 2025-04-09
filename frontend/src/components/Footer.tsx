import React from 'react';
import { FooterContainer, Link } from '../styles/components/Footer.styles';

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