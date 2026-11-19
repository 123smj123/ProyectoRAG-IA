import { useQuery } from '@tanstack/react-query'
import { getHealth } from './services/health.ts'

function App() {
  const { data, isPending, isError } = useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
  })

  return (
    <main className="mx-auto max-w-3xl p-8">
      <h1 className="text-3xl font-semibold">Proyecto RAG - IA</h1>
      <p className="mt-4">
        Estado del backend:{' '}
        {isPending ? 'comprobando…' : isError ? 'no disponible' : data.status}
      </p>
    </main>
  )
}

export default App