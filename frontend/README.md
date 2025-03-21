# Wordle Solver Frontend

A React-based web interface for the Wordle Solver application.

## Prerequisites

- Node.js (v16.x or higher)
- npm (v8.x or higher)

## Setup

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Create a `.env` file in the root directory and add:
   ```
   REACT_APP_API_URL=http://localhost:3001
   REACT_APP_ENV=development
   ```

## Available Scripts

- `npm start`: Runs the app in development mode at [http://localhost:3000](http://localhost:3000)
- `npm test`: Launches the test runner in interactive watch mode
- `npm run build`: Builds the app for production to the `build` folder
- `npm run lint`: Runs ESLint to check for code style issues
- `npm run lint:fix`: Automatically fixes ESLint issues when possible

## Project Structure

```
frontend/
├── public/              # Static files
├── src/                # Source code
│   ├── components/     # Reusable UI components
│   ├── pages/         # Page components
│   ├── services/      # API and other services
│   ├── types/         # TypeScript type definitions
│   ├── App.tsx        # Root component
│   └── index.tsx      # Entry point
├── .env               # Environment variables
├── .gitignore        # Git ignore rules
├── package.json      # Dependencies and scripts
└── tsconfig.json    # TypeScript configuration
```

## Environment Variables

- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_ENV`: Current environment (development/production)
- `REACT_APP_VERSION`: Application version from package.json

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

MIT 