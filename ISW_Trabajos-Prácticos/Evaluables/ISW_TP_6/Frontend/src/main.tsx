import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { EcoParkApp } from './EcoParkApp'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <EcoParkApp />
  </StrictMode>,
)
