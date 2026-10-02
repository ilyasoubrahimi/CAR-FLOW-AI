# Marrakech Drive - Project Guide

## Project Vision
A premium, AI-powered car rental digital experience. Not a template, but a high-end technology product.

## Tech Stack
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **State**: Zustand
- **i18n**: French (Default), English, Arabic (RTL)

## Build & Development Commands
- `cd app && npm run dev` - Start development server
- `cd app && npm run build` - Production build
- `cd app && npm run lint` - Linting check

## Architectural Standards
- **Decoupled Brand**: Company name, colors, and logos must be in a configuration file/service, not hard-coded in UI.
- **Service Layer**: All business logic (Pricing, Availability, Reservations) must reside in `src/services/`, not in components.
- **Premium UX**:
    - High whitespace, strong typography.
    - Subtle micro-interactions.
    - Mobile-first design.
- **Interface-First**: Use clean TS interfaces for all services to allow easy backend swapping.

## Current Progress
- [x] Project Initialization (Next.js)
- [ ] Design System Setup
- [ ] Core Service Layer (Pricing, Vehicles)
- [ ] Customer Journey Implementation
- [ ] Admin Dashboard
- [ ] AI Assistant Integration
- [ ] Multi-language Support
- [ ] SEO & Final Polish
