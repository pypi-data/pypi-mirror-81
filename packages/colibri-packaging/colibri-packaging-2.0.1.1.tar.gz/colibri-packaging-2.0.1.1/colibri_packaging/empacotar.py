# coding: utf-8
from __future__ import print_function
import json
import logging
import os
import subprocess
import re
import sys
import shutil
try:
    from scripts.versao_banco import obter_versao_db_scripts
except ImportError:
    obter_versao_db_scripts = None

PY3 = sys.version_info > (3,)
if PY3:
    from functools import cmp_to_key
CAM_7ZA = os.path.join(os.path.split(__file__)[0] or os.getcwd(), '7za.exe')
MANIFESTO_SERVER = 'manifesto.server'
MANIFESTO_LOCAL = 'manifesto.local'
MANIFESTO = 'manifesto.dat'
EXTENSAO_PACOTE = '.cmpkg'
RE_ARQ_SCRIPT = re.compile(r'_scripts(\d{0,2})(\S+)?\.zip')
EXTENSAO_ARQ_SCRIPT = '.zip'
PACOTE = 'nome'
VERSAO = 'versao'
SCHEMA = 'schema'
ARQUIVOS = 'arquivos'
NOME_ARQ = 'nome'
MENSAGEM = 'mensagem'
DESTINO = 'destino'
DEVELOP = 'develop'
INNOSERV = 'innoserv'
BASES_COMPATIVEIS = 'versoes_bases'
ARQ_PACOTE = 'pacote'
ARQ_SCRIPTS = 'scripts'
ARQ_CLIENT = 'client'
ARQ_SERVIDOR = 'server'
ARQ_SHARED = 'shared'
PASTA_QA = r'd:\Builder\QA'


logger = logging.getLogger('empacotar')

DEFAULTS_PACOTE = dict(
    versao="1.0.0.0"
)
_ordem_arquivo = dict()


def _acha_ordem(arq):
    def _obter_sequencia():
        def_ret = _ordem_arquivo.get(arq['nome'], 0)
        if arq['destino'] == ARQ_SCRIPTS:
            match = RE_ARQ_SCRIPT.match(arq['nome'])
            if match and match.group(1):
                def_ret = int(match.group(1))
        return def_ret

    ordem = {
        ARQ_PACOTE: -1000,
        ARQ_SCRIPTS: 0,
        ARQ_SHARED: 1000,
        ARQ_SERVIDOR: 2000,
        ARQ_CLIENT: 3000
    }

    return ordem.get(arq['destino']) + _obter_sequencia()


def _acha_tipo(arqorg):
    arqorg = arqorg.lower()
    if RE_ARQ_SCRIPT.match(arqorg):
        return ARQ_SCRIPTS


def _obter_chaves_arquivo(dict_chaves):
    return {chave: valor for chave, valor in dict_chaves.items() if
            chave != 'nome' and not chave.startswith('_')}


def _excluir_com_prefixo(pasta, prefixo):
    for arq in os.listdir(pasta):
        if arq.endswith(EXTENSAO_PACOTE) and arq.startswith(prefixo):
            try:
                os.unlink(os.path.join(pasta, arq))
            except Exception:
                logger.exception('Falha ao remover cmpkg anterior: ' + arq)


def obter_arquivos(pasta, configs):
    lista_zip = list((os.path.join(pasta, MANIFESTO),))
    lista_anterior = configs.get(ARQUIVOS, list())

    configs[ARQUIVOS] = list()

    for arq in os.listdir(pasta):
        if arq.lower() == MANIFESTO:
            continue

        dictarq = dict(
            nome=arq
        )

        # se eu encontrar a definição do arquivo na lista anterior,
        # uso o que eu encontrar
        for pos, a in enumerate(lista_anterior):
            if '_pattern_nome' in a and re.match(a['_pattern_nome'], arq):
                if "__count" in a:
                    a["__count"] += 1
                else:
                    a["__count"] = 1
                dictarq.update(_obter_chaves_arquivo(a))
                _ordem_arquivo[arq] = pos
                break

        # só considero os arquivos do manifesto e os parametrizados
        if dictarq.get('destino') is None:
            dictarq['destino'] = _acha_tipo(arq)

        if dictarq.get('destino'):
            configs[ARQUIVOS].append(dictarq)
            lista_zip.append(os.path.join(pasta, arq))
        elif arq.lower().endswith('.exe'):
            raise RuntimeError(
                f"Arquivo executável desconhecido na pasta de empacotamento: {arq}"
            )

    for a in lista_anterior:
        if '_pattern_nome' in a and "__count" not in a:
            raise RuntimeError(
                f"Pattern de nome arquivo não foi encontrado: {a['_pattern_nome']}"
            )

    if PY3:
        configs[ARQUIVOS].sort(
            key=cmp_to_key(
                lambda arq1, arq2: _acha_ordem(arq1) - _acha_ordem(arq2)
            )
        )
    else:
        configs[ARQUIVOS].sort(
            cmp=lambda arq1, arq2: _acha_ordem(arq1) - _acha_ordem(arq2)
        )
    return lista_zip


def obter_versoes_bases(configs, kwargs):
    OBTER = '_obter_versao_do_json'
    versoes_bases = [
        dict(schema=a[0], versao=a[1]) for a in kwargs.pop('versoes_bases', [])
    ]
    schemas = [a[SCHEMA] for a in versoes_bases]

    for base in configs.get(BASES_COMPATIVEIS, []):
        obter = base.get(OBTER)
        if obter:
            if obter_versao_db_scripts is None:
                raise RuntimeError('Biblioteca de scripts indisponivel')
            schema, versao = obter_versao_db_scripts(obter)
            base[SCHEMA] = schema
            base[VERSAO] = versao
            del base[OBTER]
        if base.get(SCHEMA) and base.get(SCHEMA) not in schemas:
            versoes_bases.append(base)

    if len(versoes_bases):
        configs[BASES_COMPATIVEIS] = versoes_bases


def empacotar(pasta, pasta_saida, senha, **kwargs):
    try:
        manifesto_usado = os.path.join(pasta, MANIFESTO_SERVER)
        with open(manifesto_usado, 'r', encoding='utf-8-sig') as arq:
            configs = json.load(arq)
            logger.info('usando ' + MANIFESTO_SERVER)
    except IOError:
        try:
            manifesto_usado = os.path.join(pasta, MANIFESTO_LOCAL)
            with open(manifesto_usado, 'r', encoding='utf-8-sig') as arq:
                configs = json.load(arq)
                logger.info('usando ' + MANIFESTO_LOCAL)
        except IOError:
            logger.info(u'template de manifesto não encontrado. gerando...')
            configs = DEFAULTS_PACOTE.copy()
    except Exception as e:
        logger.exception('Erro ao processar manifesto %s', manifesto_usado)
        print('Erro ao processar: ' + manifesto_usado)
        print(e)
        raise

    # Atualizo o manifesto com o que foi passado pela linha de comando
    obter_versoes_bases(configs, kwargs)
    configs.update(kwargs)

    arquivos = obter_arquivos(pasta, configs)

    with open(os.path.join(pasta, MANIFESTO), 'w') as manifile:
        json.dump(configs, manifile, indent=2)

    prefixo = configs[PACOTE].replace(' ', '') + '_'
    nome_cmpkg = prefixo + \
        configs[VERSAO].replace(' ', '').replace('.', '_') + \
        EXTENSAO_PACOTE
    saida = os.path.join(pasta_saida, nome_cmpkg)

    _excluir_com_prefixo(pasta_saida, prefixo)
    zipar(saida, arquivos=arquivos, senha=senha)
    arquivo_cmpkg = os.path.join(os.getcwd(), saida)

    # Suporte a uma pasta para os QAs
    if os.environ.get('QA', '').lower() == 'true':
        if os.environ.get('ALOHA', '').lower() == 'true':
            logger.error('Arquivo não será gerado na pasta de QA pois ALOHA=true')
            return
        pasta_QA = os.environ.get('PASTA_QA', PASTA_QA)
        if not os.path.exists(pasta_QA):
            logger.error(f'PASTA_QA nao encontrada: {pasta_QA}')
        else:
            _excluir_com_prefixo(pasta_QA, prefixo)
            try:
                print(f'Copiando para pasta de QA: {pasta_QA}')
                shutil.copyfile(saida, os.path.join(pasta_QA, nome_cmpkg))
            except Exception:
                logger.exception(
                    f'Falha ao copiar arquivo {saida} para a pasta {pasta_QA}'
                )

    return arquivo_cmpkg


def zipar(destino, arquivos=None, pasta=None, senha=''):
    destino = os.path.join(os.getcwd(), destino)

    cmdline = [
        CAM_7ZA,
        'a',
        '-tzip',
        '-mx9',
        '-y'
    ]
    if senha:
        cmdline.append('-p' + senha)
    cmdline.append(destino)

    if arquivos:
        cmdline = cmdline + arquivos
        prevdir = None
    elif pasta:
        prevdir = os.getcwd()
        pasta = os.path.join(os.getcwd(), pasta)
        os.chdir(pasta)

    logger.debug('comando gerado: "{}"'.format(cmdline))
    subprocess.call(cmdline)
    if prevdir:
        os.chdir(prevdir)
