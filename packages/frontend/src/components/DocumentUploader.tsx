import { useState, useCallback } from 'react';
import {
  makeStyles,
  tokens,
  Button,
  Text,
  Card,
  Badge,
  Spinner,
} from '@fluentui/react-components';
import {
  ArrowUploadRegular,
  DocumentRegular,
  DeleteRegular,
  CheckmarkCircleRegular,
  ErrorCircleRegular,
} from '@fluentui/react-icons';

const useStyles = makeStyles({
  container: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  dropzone: {
    border: `2px dashed ${tokens.colorNeutralStroke1}`,
    borderRadius: tokens.borderRadiusMedium,
    padding: '32px',
    textAlign: 'center',
    backgroundColor: tokens.colorNeutralBackground2,
    cursor: 'pointer',
    transition: 'all 0.2s',
    ':hover': {
      borderColor: tokens.colorBrandBackground,
      backgroundColor: tokens.colorNeutralBackground1,
    },
  },
  dropzoneActive: {
    borderColor: tokens.colorBrandBackground,
    backgroundColor: tokens.colorBrandBackground2,
  },
  uploadIcon: {
    fontSize: '48px',
    color: tokens.colorNeutralForeground3,
    marginBottom: '16px',
  },
  fileList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  fileCard: {
    padding: '12px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: '12px',
  },
  fileInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    flex: 1,
  },
  fileDetails: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
  },
  fileActions: {
    display: 'flex',
    gap: '8px',
  },
  hiddenInput: {
    display: 'none',
  },
});

export interface UploadedFile {
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress?: number;
  error?: string;
}

interface DocumentUploaderProps {
  files: UploadedFile[];
  onFilesChange: (files: UploadedFile[]) => void;
  maxFiles?: number;
  acceptedTypes?: string[];
}

export function DocumentUploader({
  files,
  onFilesChange,
  maxFiles = 10,
  acceptedTypes = ['.pdf', '.txt', '.md', '.doc', '.docx'],
}: DocumentUploaderProps) {
  const styles = useStyles();
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);

      const droppedFiles = Array.from(e.dataTransfer.files);
      const newFiles: UploadedFile[] = droppedFiles
        .filter((file) => {
          // Verificar tipo de arquivo
          const extension = '.' + file.name.split('.').pop()?.toLowerCase();
          return acceptedTypes.includes(extension);
        })
        .slice(0, maxFiles - files.length)
        .map((file) => ({
          file,
          status: 'pending' as const,
        }));

      onFilesChange([...files, ...newFiles]);
    },
    [files, onFilesChange, maxFiles, acceptedTypes]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFiles = Array.from(e.target.files || []);
      const newFiles: UploadedFile[] = selectedFiles
        .slice(0, maxFiles - files.length)
        .map((file) => ({
          file,
          status: 'pending' as const,
        }));

      onFilesChange([...files, ...newFiles]);
      e.target.value = ''; // Reset input
    },
    [files, onFilesChange, maxFiles]
  );

  const handleRemoveFile = useCallback(
    (index: number) => {
      const newFiles = files.filter((_, i) => i !== index);
      onFilesChange(newFiles);
    },
    [files, onFilesChange]
  );

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const getStatusIcon = (status: UploadedFile['status']) => {
    switch (status) {
      case 'uploading':
        return <Spinner size="tiny" />;
      case 'success':
        return <CheckmarkCircleRegular fontSize={20} style={{ color: tokens.colorPaletteGreenForeground1 }} />;
      case 'error':
        return <ErrorCircleRegular fontSize={20} style={{ color: tokens.colorPaletteRedForeground1 }} />;
      default:
        return <DocumentRegular fontSize={20} />;
    }
  };

  const getStatusBadge = (status: UploadedFile['status']) => {
    switch (status) {
      case 'uploading':
        return <Badge appearance="tint" color="informative">Enviando...</Badge>;
      case 'success':
        return <Badge appearance="tint" color="success">Enviado</Badge>;
      case 'error':
        return <Badge appearance="tint" color="danger">Erro</Badge>;
      default:
        return <Badge appearance="tint">Pendente</Badge>;
    }
  };

  return (
    <div className={styles.container}>
      <div
        className={`${styles.dropzone} ${isDragging ? styles.dropzoneActive : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => document.getElementById('file-input')?.click()}
      >
        <ArrowUploadRegular className={styles.uploadIcon} />
        <Text weight="semibold" size={400}>
          Arraste arquivos aqui ou clique para selecionar
        </Text>
        <Text size={300} style={{ color: tokens.colorNeutralForeground3, marginTop: '8px' }}>
          Tipos aceitos: {acceptedTypes.join(', ')}
        </Text>
        <Text size={200} style={{ color: tokens.colorNeutralForeground3 }}>
          Máximo: {maxFiles} arquivos
        </Text>
      </div>

      <input
        id="file-input"
        type="file"
        multiple
        accept={acceptedTypes.join(',')}
        onChange={handleFileSelect}
        className={styles.hiddenInput}
      />

      {files.length > 0 && (
        <div className={styles.fileList}>
          <Text weight="semibold">
            Arquivos anexados ({files.length}/{maxFiles})
          </Text>
          
          {files.map((uploadedFile, index) => (
            <Card key={index} className={styles.fileCard}>
              <div className={styles.fileInfo}>
                {getStatusIcon(uploadedFile.status)}
                
                <div className={styles.fileDetails}>
                  <Text weight="semibold">{uploadedFile.file.name}</Text>
                  <Text size={200} style={{ color: tokens.colorNeutralForeground3 }}>
                    {formatFileSize(uploadedFile.file.size)}
                  </Text>
                </div>

                {getStatusBadge(uploadedFile.status)}
              </div>

              <div className={styles.fileActions}>
                {uploadedFile.status !== 'uploading' && (
                  <Button
                    appearance="subtle"
                    icon={<DeleteRegular />}
                    onClick={() => handleRemoveFile(index)}
                    size="small"
                  />
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
