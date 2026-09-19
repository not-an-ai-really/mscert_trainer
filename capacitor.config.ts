import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.notanai.mscerttrainer',
  appName: 'MS-Cert Trainer',
  webDir: 'phone-pwa',
  backgroundColor: '#0b1026',
  server: {
    androidScheme: 'https',
  },
  ios: {
    contentInsetMode: 'resize',
  },
  android: {
    allowMixedContent: false,
  },
};

export default config;
