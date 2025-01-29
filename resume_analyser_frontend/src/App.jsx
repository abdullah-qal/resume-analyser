import { useState } from 'react'
import './App.css'
import ResumeUpload from './components/ResumeUpload'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="flex justify-center items-center min-h-screen">
      <ResumeUpload />
    </div>
  )
}

export default App
