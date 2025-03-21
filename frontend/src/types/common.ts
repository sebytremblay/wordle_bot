export type FeedbackType = 0 | 1 | 2;

export interface Theme {
    colors: {
        primary: string;
        primaryDark: string;
        secondary: string;
        gray: string;
        border: string;
        text: string;
        error: string;
        white: string;
    };
}

export class APIError extends Error {
    constructor(
        message: string,
        public status?: number,
        public data?: any
    ) {
        super(message);
        this.name = 'APIError';
    }
} 