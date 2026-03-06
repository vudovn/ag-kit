import { render, screen } from '@testing-library/react'
import { Sidebar } from '@/components/Sidebar'
import { usePathname } from 'next/navigation'

// Mock usePathname
jest.mock('next/navigation', () => ({
  ...jest.requireActual('next/navigation'),
  usePathname: jest.fn(),
}))

describe('Sidebar', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('should render sidebar with logo', () => {
    ;(usePathname as jest.Mock).mockReturnValue('/')
    
    render(<Sidebar />)
    
    expect(screen.getByText('LUNA OS')).toBeInTheDocument()
    expect(screen.getByText('Haven Soberana')).toBeInTheDocument()
  })

  it('should render main navigation items', () => {
    ;(usePathname as jest.Mock).mockReturnValue('/')
    
    render(<Sidebar />)
    
    expect(screen.getByText('Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Conversas')).toBeInTheDocument()
    expect(screen.getByText('Analytics')).toBeInTheDocument()
    expect(screen.getByText('Clientes')).toBeInTheDocument()
    expect(screen.getByText('Campanhas')).toBeInTheDocument()
    expect(screen.getByText('Dojo Arena')).toBeInTheDocument()
    expect(screen.getByText('Brain')).toBeInTheDocument()
    expect(screen.getByText('Intelligence')).toBeInTheDocument()
    expect(screen.getByText('Persona')).toBeInTheDocument()
  })

  it('should render catálogo section', () => {
    ;(usePathname as jest.Mock).mockReturnValue('/')
    
    render(<Sidebar />)
    
    expect(screen.getByText('Serviços')).toBeInTheDocument()
    expect(screen.getByText('Profissionais')).toBeInTheDocument()
    expect(screen.getByText('Pacotes')).toBeInTheDocument()
  })

  it('should highlight active navigation item', () => {
    ;(usePathname as jest.Mock).mockReturnValue('/conversations')
    
    render(<Sidebar />)
    
    const conversationsLink = screen.getByText('Conversas').closest('a')
    expect(conversationsLink).toHaveClass('bg-grad-premium')
  })

  it('should show LIVE badge on Conversas', () => {
    ;(usePathname as jest.Mock).mockReturnValue('/')
    
    render(<Sidebar />)
    
    expect(screen.getByText('LIVE')).toBeInTheDocument()
  })

  it('should show PRO badge on Analytics', () => {
    ;(usePathname as jest.Mock).mockReturnValue('/')
    
    render(<Sidebar />)
    
    expect(screen.getByText('PRO')).toBeInTheDocument()
  })

  it('should render connection status footer', () => {
    ;(usePathname as jest.Mock).mockReturnValue('/')
    
    render(<Sidebar />)
    
    expect(screen.getByText('Cérebro Luna v2.0')).toBeInTheDocument()
    expect(screen.getByText('Protocolo Sync Ativo')).toBeInTheDocument()
  })
})
