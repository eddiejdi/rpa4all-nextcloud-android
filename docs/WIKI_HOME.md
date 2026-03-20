# RPA4All Nextcloud Android - Wiki

## Entregas

- Fork nativo Android: `com.rpa4all.nextcloud`
- Servidor fixo sem digitar URL: `https://nextcloud.rpa4all.com`
- Branding: nome, launcher icon e cores iniciais
- Compatibilidade com login OIDC/Authentik no servidor Nextcloud
- Release APK publicada no GitHub Releases

## Build local

```bash
export ANDROID_HOME=/home/edenilson/android-sdk
export ANDROID_SDK_ROOT=/home/edenilson/android-sdk
./gradlew :app:assembleRpa4allRelease --no-daemon --console=plain --max-workers=2 \
  -Dkotlin.compiler.execution.strategy=in-process \
  -Dorg.gradle.jvmargs='-Xmx2048m -XX:MaxMetaspaceSize=768m'
```

APK gerado em:

`app/build/outputs/apk/rpa4all/release/rpa4all-release-330010000.apk`

## Assinatura do APK

Foi gerado um APK assinado para distribuição com `jarsigner`, arquivo final:

`app/build/outputs/apk/rpa4all/release/rpa4all-nextcloud-android-v1.0.0.apk`

## Publicação

- Repositório: `https://github.com/eddiejdi/rpa4all-nextcloud-android`
- Release: `https://github.com/eddiejdi/rpa4all-nextcloud-android/releases/tag/v1.0.0`
- Asset APK:
  `https://github.com/eddiejdi/rpa4all-nextcloud-android/releases/download/v1.0.0/rpa4all-nextcloud-android-v1.0.0.apk`

## Google Play

Fluxo preparado para publicação no app `com.rpa4all.nextcloud`:

- Build de AAB: `scripts/release/build_rpa4all_play_artifacts.sh`
- Upload via API Play: `scripts/release/upload_rpa4all_play.py`
- Guia completo: `docs/GOOGLE_PLAY_DEPLOY_RPA4ALL.md`
- Política de privacidade (GitHub Pages): `https://eddiejdi.github.io/rpa4all-nextcloud-android/`

## Authentik (`auth.rpa4all.com`)

Template customizado:

`tools/authentik_management/templates/base/skeleton.html`

Inclui:

- Link direto Android (APK personalizado)
- Link Apple (App Store Nextcloud oficial)
- Submenu no contexto "More Details" para Nextcloud

## Observações iOS

Para iOS personalizado é necessário pipeline Apple (Apple Developer Team + assinatura + publicação).  
Atualmente o link Apple aponta para o app oficial da App Store.
