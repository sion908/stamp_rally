// script.ts
import { load } from 'js-yaml'
import { readFileSync } from 'fs'

interface dict{[key:string]: string}

interface EnvironmentConfig {
    [key: string]: string | number | dict;
}

export const ENVS = {
    DEV: 'dev',
    TEST: 'test',
    STAGING: 'staging',
    PROD: 'prod',
    LOCAL: 'local'
}

export const getConfig = (env:string): { [key: string]: string; }| null =>
{
    try {
        // yamlファイルの読み込み
        const config = load(readFileSync('./lib/.env.yaml', 'utf8')) as EnvironmentConfig

        for (let key in config) {
            // valueがデータであればそのまま、dictであれば、対象の環境ごとに戻り値を入れる
            switch (typeof config[key]) {
                case "string":
                case "number":
                    break;
                // dictであった場合は、keyに現環境が含まれているか確認し、なければdefaultのvalueを代入する
                case "object":
                    const each_env = config[key] as dict
                    config[key] = String(Object.keys(each_env).includes(env)? each_env[env]: each_env['default'])
                    if(!config[key]){
                        // 値が設定されていない場合の例外処理
                        throw new Error("環境変数が設定されていません");
                    }
                    break;
            }

        }

        return config as { [key: string]: string; }
    } catch (err: unknown) {
        if (err instanceof Error) {
          console.error(err.message);
        }
        return null
    }
}
