import Header from './Header'

export default function Layout({ children, darkMode, setDarkMode, showBack, onBack }) {
  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
        <Header darkMode={darkMode} setDarkMode={setDarkMode} showBack={showBack} onBack={onBack} />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6">
          {children}
        </main>
      </div>
    </div>
  )
}
