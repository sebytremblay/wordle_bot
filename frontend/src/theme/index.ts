import { DefaultTheme } from 'styled-components';
import { Theme } from '../types/common';

declare module 'styled-components' {
    export interface DefaultTheme extends Theme { }
}

export const theme: DefaultTheme = {
    colors: {
        primary: '#6aaa64',
        primaryDark: '#538d4e',
        secondary: '#c9b458',
        gray: '#787c7e',
        border: '#d3d6da',
        text: '#1a1a1b',
        error: '#ff0000',
        white: '#ffffff',
    },
}; 