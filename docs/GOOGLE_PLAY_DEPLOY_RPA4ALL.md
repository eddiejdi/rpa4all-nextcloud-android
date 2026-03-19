# Google Play Deploy (RPA4All)

## App

- Package: `com.rpa4all.nextcloud`
- Name: `NextCloud by RPA4All`

## Pre-requisitos

1. Conta Play Console com app criado para `com.rpa4all.nextcloud`.
2. Service Account com permissão de release no app.
3. JSON da Service Account local (exemplo: `~/.secrets/google-play-rpa4all.json`).
4. Keystore de upload da Play (a mesma registrada no app).

## Build AAB

```bash
cd /home/edenilson/eddie-auto-dev/forks/rpa4all-nextcloud-android
chmod +x scripts/release/build_rpa4all_play_artifacts.sh
scripts/release/build_rpa4all_play_artifacts.sh
```

Artefatos:

- `release-play/app-rpa4all-release-unsigned.aab`
- `release-play/app-rpa4all-release-signed.aab` (se variáveis de assinatura estiverem definidas)

## Assinatura (opcional no script de build)

Definir antes do build:

```bash
export RPA4ALL_KEYSTORE_FILE="/caminho/rpa4all-upload.jks"
export RPA4ALL_KEYSTORE_PASSWORD="***"
export RPA4ALL_KEY_ALIAS="***"
export RPA4ALL_KEY_PASSWORD="***"
```

## Upload para Play (track internal/beta/production)

Instalar dependências:

```bash
pip install google-api-python-client google-auth
```

Executar upload:

```bash
python3 scripts/release/upload_rpa4all_play.py \
  --service-account-json ~/.secrets/google-play-rpa4all.json \
  --aab release-play/app-rpa4all-release-signed.aab \
  --package-name com.rpa4all.nextcloud \
  --track internal \
  --status completed
```

## Observações

- Sem a keystore correta de upload, a Play rejeita o AAB.
- Sem service account com acesso ao app, o upload falha com permissão.
