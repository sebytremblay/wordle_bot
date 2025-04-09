import styled from '@emotion/styled';
import { theme } from '../theme';

export const FooterContainer = styled.footer`
    display: flex;
    justify-content: center;
    align-items: center;
    padding: ${theme.spacing.sm};
    margin-top: ${theme.spacing.lg};
    border-top: 1px solid ${theme.colors.border};
    color: ${theme.colors.text.secondary};
    font-size: ${theme.typography.fontSizes.small};
`;

export const Link = styled.a`
    color: ${theme.colors.primaryHover};
    text-decoration: none;
    margin: 0 ${theme.spacing.xs};
    
    &:hover {
        text-decoration: underline;
    }
`; 