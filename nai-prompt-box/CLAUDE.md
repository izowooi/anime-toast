# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NAI Prompt Box is a React-based web application for managing and copying NovelAI art prompt tags. The application provides an interface with collapsible categories where users can click buttons to copy pre-configured prompt strings to their clipboard.

## Development Commands

```bash
# Start development server (opens at http://localhost:3000)
npm start

# Run tests in interactive watch mode
npm test

# Run tests for a specific file
npm test -- <filename>

# Build for production (outputs to build/ folder)
npm run build
```

## Deployment

The project is configured for Firebase Hosting:
- Build output directory: `build/`
- All routes are rewritten to `/index.html` for client-side routing support
- Deploy after building: `firebase deploy` (requires Firebase CLI)

## Architecture

### Component Structure

The app follows a simple hierarchical component structure:

```
App (root)
├── Header (static branding)
├── CategorySection (collapsible category container)
│   └── TagButton (individual tag with copy functionality)
└── Toast (notification system for user feedback)
```

### Data Flow

1. **Tag Data**: Centralized in [src/data/tags.js](src/data/tags.js) as exported objects where keys are button labels and values are the prompt strings to copy
2. **Copy Mechanism**: Uses the Clipboard API (`navigator.clipboard.writeText`) in [TagButton.js:7](src/components/TagButton.js#L7)
3. **User Feedback**: Toast notification system managed via state in [App.js:9-10](src/app.js#L9-L10), triggered by the `onCopy` callback pattern

### State Management

No external state management library is used. State is managed with React hooks:
- Local component state for UI interactions (expand/collapse in CategorySection)
- Lifted state in App component for cross-component communication (toast notifications)

## Adding New Tag Categories

To add a new category:

1. Define the tag object in [src/data/tags.js](src/data/tags.js):
   ```javascript
   export const newCategoryTags = {
     '라벨1': 'prompt string 1',
     '라벨2': 'prompt string 2'
   };
   ```

2. Import and render in [src/App.js](src/App.js):
   ```javascript
   import { artTags, newCategoryTags } from './data/tags';

   // In JSX:
   <CategorySection
     categoryName="새 카테고리"
     tags={newCategoryTags}
     onCopy={handleCopy}
   />
   ```

## Technology Stack

- React 19.2.0 with hooks
- Create React App (standard configuration, not ejected)
- Firebase Hosting for deployment
- No UI framework or component library
