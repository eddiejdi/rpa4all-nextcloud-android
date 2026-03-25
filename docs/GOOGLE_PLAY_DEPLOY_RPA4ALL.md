# Google Play Deploy (RPA4All)

## App

- Package: `com.rpa4all.nextcloud`
- Name: `Nextcloud -by RPA4All`
- Metadata da ficha Play: `src/rpa4all/fastlane/metadata`

## Pre-requisitos

1. Conta Play Console com app criado para `com.rpa4all.nextcloud`.
2. Service Account com permissão de release no app.
3. Para atualizar descrição, screenshots e assets da ficha, a conta também precisa de permissão de Store Presence / App content no Play Console.
4. JSON da Service Account local (exemplo: `~/.secrets/google-play-rpa4all.json`).
5. Keystore de upload da Play (a mesma registrada no app).

## GitHub Actions (publicacao automatica)

Configurar os seguintes secrets no repositorio:

- `RPA4ALL_KEYSTORE_BASE64`: keystore JKS em base64
- `RPA4ALL_KEYSTORE_STOREPASS`: senha do keystore
- `RPA4ALL_KEYSTORE_KEYPASS`: senha da chave
- `RPA4ALL_KEYSTORE_ALIAS`: alias da chave
- `RPA4ALL_PLAY_SERVICE_ACCOUNT_JSON_B64`: JSON da service account em base64
- `TELEGRAM_BOT_TOKEN` (opcional): token do bot Telegram para notificações
- `TELEGRAM_CHAT_ID` (opcional): ID do chat/group Telegram para receber link de internal testing

Depois disso, execute o workflow `.github/workflows/publish-rpa4all.yml` com `track=internal`.

### Notas sobre Telegram (opcional)
- Se `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` forem configurados, você receberá um link de instalação no Telegram após cada publicação bem-sucedida no track internal.
- Para obter o bot token, converse com `@BotFather` no Telegram.
- Para obter o chat ID, encaminhe uma mensagem para `@JsonDumpBot` e procure o campo `from.id`.

## Build AAB

```bash
cd /home/edenilson/eddie-auto-dev/forks/rpa4all-nextcloud-android
chmod +x scripts/release/build_rpa4all_play_artifacts.sh
scripts/release/build_rpa4all_play_artifacts.sh
```

Artefatos:

- `release-play/app-rpa4all-release-unsigned.aab`
- `release-play/app-rpa4all-release-signed.aab` (se variáveis de assinatura estiverem definidas)

## Ficha da Play Store

Gerar ou atualizar os assets locais da ficha:

```bash
cd /home/edenilson/eddie-auto-dev/forks/rpa4all-nextcloud-android
chmod +x scripts/release/render_rpa4all_play_assets.sh
scripts/release/render_rpa4all_play_assets.sh
```

Estrutura usada pelo upload:

- `src/rpa4all/fastlane/metadata/config.json`
- `src/rpa4all/fastlane/metadata/pt-BR/{title,short_description,full_description}.txt`
- `src/rpa4all/fastlane/metadata/en-US/{title,short_description,full_description}.txt`
- `src/rpa4all/fastlane/metadata/<locale>/images/icon.png`
- `src/rpa4all/fastlane/metadata/<locale>/images/featureGraphic.png`
- `src/rpa4all/fastlane/metadata/<locale>/images/phoneScreenshots/*.png`

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
  --metadata-dir src/rpa4all/fastlane/metadata \
  --package-name com.rpa4all.nextcloud \
  --track internal \
  --status completed
```

Atualizar somente a ficha da loja, sem novo build:

```bash
python3 scripts/release/upload_rpa4all_play.py \
  --service-account-json ~/.secrets/google-play-rpa4all.json \
  --metadata-dir src/rpa4all/fastlane/metadata \
  --package-name com.rpa4all.nextcloud
```

## Observações

- Sem a keystore correta de upload, a Play rejeita o AAB.
- Sem service account com acesso ao app, o upload falha com permissão.
- O script atualiza título, descrições, contato, ícone, feature graphic e screenshots por locale.
- Se o `commit` do edit retornar `403 The caller does not have permission`, a Service Account ainda não tem permissão suficiente para Store Presence no app.
- A URL da política de privacidade usada no app e na ficha é `https://eddiejdi.github.io/rpa4all-nextcloud-android/`.
- Link para testers (internal testing): `https://play.google.com/apps/testing/com.rpa4all.nextcloud`
  - O app aparece para instalacao depois do primeiro upload bem-sucedido no track `internal`.
