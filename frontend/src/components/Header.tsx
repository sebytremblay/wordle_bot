import React from 'react';
import { HeaderContainer, Title, Subtitle } from '@/styles/components/Header.styles';

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

const Header: React.FC<HeaderProps> = ({ title, subtitle }) => (
  <HeaderContainer>
    <Title>{title || ''}</Title>
    <Subtitle>{subtitle || ''}</Subtitle>
  </HeaderContainer>
);

export default Header; 