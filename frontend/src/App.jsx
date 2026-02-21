import { useEffect, useMemo, useState } from 'react'
import './App.css'

const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

const dateTimeFormatter = new Intl.DateTimeFormat('pt-BR', {
  dateStyle: 'short',
  timeStyle: 'short',
})

const dateFormatter = new Intl.DateTimeFormat('pt-BR', {
  dateStyle: 'short',
})

function formatCurrency(value) {
  const numberValue = Number(value ?? 0)
  return currencyFormatter.format(Number.isNaN(numberValue) ? 0 : numberValue)
}

function formatDateTime(value) {
  if (!value) {
    return '—'
  }
  return dateTimeFormatter.format(new Date(value))
}

function formatDate(value) {
  if (!value) {
    return '—'
  }
  return dateFormatter.format(new Date(value))
}

function getStatusBadgeClass(status) {
  const key = String(status || '').toLowerCase()
  if (key === 'aberto') return 'badge-aberto'
  if (key === 'cancelado') return 'badge-cancelado'
  if (key === 'entregue') return 'badge-entregue'
  return 'badge-fechado'
}

function App() {
  const [pedidos, setPedidos] = useState([])
  const [elapsed, setElapsed] = useState('')
  const [memoryMb, setMemoryMb] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadPedidos() {
      try {
        setLoading(true)
        setError('')
        const params = new URLSearchParams(window.location.search)
        const quantidade = params.get('q')
        const endpoint = quantidade ? `/api/pedidos/?q=${encodeURIComponent(quantidade)}` : '/api/pedidos/'
        const response = await fetch(endpoint)
        if (!response.ok) {
          throw new Error(`Erro ao carregar pedidos (${response.status})`)
        }
        const data = await response.json()
        const results = Array.isArray(data)
          ? data
          : Array.isArray(data.results)
            ? data.results
            : []

        setPedidos(results)
        setElapsed(data?.elapsed || '')
        setMemoryMb(data?.memory_mb || '')
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Erro inesperado ao buscar pedidos')
      } finally {
        setLoading(false)
      }
    }

    loadPedidos()
  }, [])

  const generatedAt = useMemo(() => dateTimeFormatter.format(new Date()), [])

  return (
    <div className="container-fluid py-3">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <div>
          <h4 className="mb-0">Casas Floripa — Relatório de Vendas</h4>
          <small className="text-muted">Gerado em {generatedAt}</small>
        </div>
        <div className="no-print">
          <span className="text-muted me-3 mono">
            {loading ? 'Carregando...' : `${pedidos.length} pedidos`}
          </span>
          {!!elapsed && (
            <a
              href="http://localhost:8000/silk/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-decoration-none"
            >
              <span className="badge bg-secondary mono me-2 metric-badge">{elapsed}s</span>
            </a>
          )}
          {!!memoryMb && (
            <span className="badge bg-info text-dark mono me-2 metric-badge">{memoryMb} MB</span>
          )}
        </div>
      </div>

      {loading && <div className="alert alert-info py-2">Carregando pedidos...</div>}
      {error && <div className="alert alert-danger py-2 mb-3">{error}</div>}

      <table className="table table-sm table-bordered align-middle">
        <thead className="table-light">
          <tr>
            <th>Pedido</th>
            <th>Cliente</th>
            <th>Status</th>
            <th className="text-end">Valor Total</th>
            <th>Data Criação</th>
          </tr>
        </thead>
        <tbody>
          {!loading && pedidos.length === 0 && (
            <tr>
              <td colSpan={5} className="text-center text-muted py-3">
                Nenhum pedido encontrado.
              </td>
            </tr>
          )}

          {pedidos.map((pedido) => (
            <tr key={pedido.id}>
              <td className="mono">{pedido.num_pedido || pedido.numero_pedido}</td>
              <td>{`${pedido.cliente_nome} ${pedido.cliente_sobrenome}`.trim()}</td>
              <td>
                <span className={`badge ${getStatusBadgeClass(pedido.status)}`}>
                  {pedido.status_display}
                </span>
              </td>
              <td className="text-end mono">{formatCurrency(pedido.valor_total)}</td>
              <td className="mono">{formatDateTime(pedido.data_criacao)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="no-print d-flex gap-2">
        <button className="btn btn-outline-secondary btn-sm mono" onClick={() => window.print()}>
          Imprimir
        </button>
      </div>
    </div>
  )
}

export default App
