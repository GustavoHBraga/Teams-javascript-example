import { Router } from 'express';
import multer from 'multer';
import { authenticate } from '../middleware/auth';
import { 
  uploadDocument, 
  getDocuments, 
  getDocumentById, 
  deleteDocument 
} from '../controllers/document.controller';

const router = Router();

// Configurar multer para upload de arquivos
const storage = multer.memoryStorage();
const upload = multer({
  storage,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB
  },
  fileFilter: (_req, file, cb) => {
    const allowedTypes = [
      'application/pdf',
      'text/plain',
      'text/markdown',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ];

    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Tipo de arquivo não suportado'));
    }
  },
});

// Todas as rotas requerem autenticação
router.use(authenticate);

// POST /bots/:botId/documents - Upload de documento
router.post('/:botId/documents', upload.single('file'), uploadDocument);

// GET /bots/:botId/documents - Listar documentos do bot
router.get('/:botId/documents', getDocuments);

// GET /documents/:id - Obter documento específico
router.get('/documents/:id', getDocumentById);

// DELETE /documents/:id - Deletar documento
router.delete('/documents/:id', deleteDocument);

export default router;
