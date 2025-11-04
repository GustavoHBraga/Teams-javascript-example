import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import {
  makeStyles,
  tokens,
  Card,
  Input,
  Textarea,
  Button,
  Dropdown,
  Option,
  Field,
  Title2,
  Spinner,
  Switch,
  Text,
} from '@fluentui/react-components';
import { botApi } from '../services/botService';
import { DocumentUploader, UploadedFile } from '../components/DocumentUploader';
import type { CreateBotInput, BotScope } from '@teams-bot/shared';

const useStyles = makeStyles({
  container: {
    padding: '24px',
    maxWidth: '800px',
    margin: '0 auto',
  },
  card: {
    padding: '24px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  actions: {
    display: 'flex',
    gap: '12px',
    justifyContent: 'flex-end',
    marginTop: '24px',
  },
});

export function BotCreator() {
  const styles = useStyles();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState<CreateBotInput>({
    name: '',
    description: '',
    instructions: '',
    scope: 'personal' as BotScope,
    config: {
      model: 'gpt-4-turbo',
      temperature: 0.7,
      maxTokens: 2000,
      enableRAG: false,
    },
    tags: [],
  });

  const [documents, setDocuments] = useState<UploadedFile[]>([]);
  const [isUploadingDocs, setIsUploadingDocs] = useState(false);

  const createMutation = useMutation({
    mutationFn: async (data: CreateBotInput) => {
      // 1. Criar o bot
      const bot = await botApi.create(data);
      
      // 2. Se houver documentos, fazer upload
      if (documents.length > 0) {
        setIsUploadingDocs(true);
        
        for (let i = 0; i < documents.length; i++) {
          const doc = documents[i];
          
          // Atualizar status para "uploading"
          setDocuments(prev => 
            prev.map((d, idx) => 
              idx === i ? { ...d, status: 'uploading' as const } : d
            )
          );

          try {
            await botApi.uploadDocument(bot.id, doc.file, {
              title: doc.file.name,
              description: `Documento de treinamento para ${bot.name}`,
            });

            // Atualizar status para "success"
            setDocuments(prev => 
              prev.map((d, idx) => 
                idx === i ? { ...d, status: 'success' as const } : d
              )
            );
          } catch (error) {
            console.error('Erro ao fazer upload do documento:', error);
            
            // Atualizar status para "error"
            setDocuments(prev => 
              prev.map((d, idx) => 
                idx === i ? { ...d, status: 'error' as const, error: 'Falha no upload' } : d
              )
            );
          }
        }
        
        setIsUploadingDocs(false);
      }

      return bot;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bots'] });
      navigate('/bots');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  return (
    <div className={styles.container}>
      <Title2 style={{ marginBottom: '24px' }}>Criar Novo Bot</Title2>

      <Card className={styles.card}>
        <form onSubmit={handleSubmit} className={styles.form}>
          <Field label="Nome do Bot" required>
            <Input
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Ex: Bot de Observabilidade"
              required
            />
          </Field>

          <Field label="Descrição" required>
            <Textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Descreva o propósito do bot..."
              rows={3}
              required
            />
          </Field>

          <Field label="Instruções para o Bot" required>
            <Textarea
              value={formData.instructions}
              onChange={(e) => setFormData({ ...formData, instructions: e.target.value })}
              placeholder="Você é um especialista em..."
              rows={5}
              required
            />
          </Field>

          <Field label="Escopo">
            <Dropdown
              value={formData.scope}
              onOptionSelect={(e, data) =>
                setFormData({ ...formData, scope: data.optionValue as BotScope })
              }
            >
              <Option value="personal">Pessoal</Option>
              <Option value="squad">Squad</Option>
              <Option value="organization">Organização</Option>
            </Dropdown>
          </Field>

          <Field label="Modelo de IA">
            <Dropdown
              value={formData.config.model}
              onOptionSelect={(e, data) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, model: data.optionValue as any },
                })
              }
            >
              <Option value="gpt-4-turbo">GPT-4 Turbo</Option>
              <Option value="gpt-4">GPT-4</Option>
              <Option value="gpt-3.5-turbo">GPT-3.5 Turbo</Option>
            </Dropdown>
          </Field>

          <Field label="Tags (separadas por vírgula)">
            <Input
              placeholder="Ex: observability, monitoring, sre"
              onChange={(e) =>
                setFormData({
                  ...formData,
                  tags: e.target.value.split(',').map((t) => t.trim()).filter(Boolean),
                })
              }
            />
          </Field>

          <Field label="Habilitar RAG (Retrieval-Augmented Generation)">
            <Switch
              checked={formData.config.enableRAG}
              onChange={(e, data) =>
                setFormData({
                  ...formData,
                  config: { ...formData.config, enableRAG: data.checked },
                })
              }
              label={
                formData.config.enableRAG
                  ? 'RAG ativado - O bot usará os documentos anexados para responder'
                  : 'RAG desativado - O bot usará apenas conhecimento base'
              }
            />
          </Field>

          {formData.config.enableRAG && (
            <Field 
              label="Documentos de Treinamento" 
              hint="Anexe documentos para o bot ter conhecimento específico do seu domínio"
            >
              <DocumentUploader
                files={documents}
                onFilesChange={setDocuments}
                maxFiles={10}
                acceptedTypes={['.pdf', '.txt', '.md', '.doc', '.docx']}
              />
            </Field>
          )}

          {documents.length > 0 && (
            <Card style={{ padding: '16px', backgroundColor: tokens.colorNeutralBackground3 }}>
              <Text weight="semibold">📚 Como funciona o RAG:</Text>
              <Text size={300} style={{ marginTop: '8px', display: 'block' }}>
                Os documentos anexados serão processados e indexados. Quando você fizer perguntas, 
                o bot vai buscar informações relevantes nesses documentos e usar como contexto para 
                gerar respostas mais precisas e específicas do seu cenário.
              </Text>
            </Card>
          )}

          <div className={styles.actions}>
            <Button onClick={() => navigate('/bots')}>Cancelar</Button>
            <Button
              type="submit"
              appearance="primary"
              disabled={createMutation.isPending || isUploadingDocs}
              icon={createMutation.isPending || isUploadingDocs ? <Spinner size="tiny" /> : undefined}
            >
              {isUploadingDocs 
                ? 'Enviando documentos...' 
                : createMutation.isPending 
                  ? 'Criando...' 
                  : 'Criar Bot'}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
