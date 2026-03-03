-- LUNA OS: Sprint 2 UX Polish & Security 
-- D5: Reforçando Integridade de Dados com CHECK Constraint
-- Data: 2026-03-03
BEGIN;
-- 1. Primeiro, atualizamos qualquer status inválido ou nulo para um valor seguro ('draft')
UPDATE public.campaigns
SET status = 'draft'
WHERE status IS NULL
    OR status NOT IN (
        'draft',
        'scheduled',
        'running',
        'paused',
        'completed',
        'cancelled',
        'failed'
    );
-- 2. Agora podemos adicionar a constraint com segurança
ALTER TABLE public.campaigns DROP CONSTRAINT IF EXISTS campaigns_status_check;
ALTER TABLE public.campaigns
ADD CONSTRAINT campaigns_status_check CHECK (
        status IN (
            'draft',
            'scheduled',
            'running',
            'paused',
            'completed',
            'cancelled',
            'failed'
        )
    );
COMMIT;