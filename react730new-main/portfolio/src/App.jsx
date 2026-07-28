import React from 'react'
import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import AboutPage from './pages/AboutPage'
import ContactPage from './pages/ContactPage'
import ProjectsPage from './pages/ProjectsPage'
import Header from './components/Header'
import Footer from './components/Footer'
import PageNotFoundPage from './pages/pageNotFoundPage'
import ProjectPage from './pages/ProjectPage'
function App() {
  return (
		<>
			<Header />
			<div className='mx-auto max-w-5xl' style={{height:"80%"}}>
				<Routes>
					<Route
						path=''
						element={<HomePage />}
					/>
					<Route
						path='/about'
						element={<AboutPage />}
					/>
					<Route
						path='/contact'
						element={<ContactPage />}
					/>
					<Route
						path='/projects'
						element={<ProjectsPage />}
				  />
				  <Route path="/project/:id" element={<ProjectPage />} />
					<Route
						path='*'
						element={<PageNotFoundPage />}
					/>
				</Routes>
			</div>
			<Footer />
		</>
	)
}

export default App
