# DoubtMate Chat - Electron App

A desktop chatbot application for the DoubtMate learning platform.

## Features

- Real-time chat with DoubtMate AI assistant
- Message history persistence
- Cross-platform desktop application
- Clean and intuitive user interface

## Development

### Prerequisites

- Node.js 16+ and npm

### Setup

1. Clone this repository
2. Navigate to the electron-app directory:
   ```
   cd frontend/electron-app
   ```
3. Install dependencies:
   ```
   npm install
   ```

### Running the Application

For development:
```
npm run dev
```

For production:
```
npm start
```

### Building the Application

```
npm run build
```

The packaged application will be available in the `dist` directory.

## Project Structure

- `/src/main` - Electron main process code
- `/src/renderer` - UI code (HTML, CSS, frontend JavaScript)
- `/src/preload` - Preload scripts for secure context bridging
- `/tests` - Test files

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
