import styled from '@emotion/styled';
import { theme } from '../theme';

export const Counter = styled.button`
    width: 100%;
    max-width: 350px;
    margin: ${theme.spacing.sm} auto;
    padding: ${theme.spacing.sm} ${theme.spacing.sm};
    background-color: ${theme.colors.background.secondary};
    border: 2px solid ${theme.colors.background.tertiary};
    border-radius: 8px;
    text-align: center;
    font-size: ${theme.typography.fontSizes.base};
    color: ${theme.colors.primaryHover};
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: ${theme.spacing.xs};
    position: relative;
    font-family: inherit;

    &:hover {
        background-color: ${theme.colors.background.tertiary};
        transform: translateY(-1px);
        box-shadow: ${theme.shadows.sm};
    }

    &:active {
        transform: translateY(0);
    }

    &::after {
        position: absolute;
        bottom: -20px;
        left: 50%;
        transform: translateX(-50%);
        font-size: ${theme.typography.fontSizes.small};
        color: ${theme.colors.text.secondary};
        opacity: 0;
        transition: opacity 0.2s ease;
    }

    &:hover::after {
        opacity: 1;
    }
`; 