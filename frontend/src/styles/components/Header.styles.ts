import styled from '@emotion/styled';
import { theme } from '../theme';

export const HeaderContainer = styled.header`
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: ${theme.spacing.sm};
    border-bottom: 1px solid ${theme.colors.border};
    margin-bottom: ${theme.spacing.lg};
`;

export const Title = styled.h1`
    font-size: ${theme.typography.fontSizes.xxlarge};
    font-weight: 700;
    margin: 0;
    color: ${theme.colors.text.primary};
    letter-spacing: 0.2rem;
`;

export const Subtitle = styled.p`
    font-size: ${theme.typography.fontSizes.base};
    color: ${theme.colors.text.secondary};
    margin: ${theme.spacing.xs} 0;
    text-align: center;
    max-width: 600px;
`; 