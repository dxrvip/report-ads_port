/* tslint:disable */
/* eslint-disable */
/**
 * report-ads_port
 * report-ads_port API
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import globalAxios, { AxiosPromise, AxiosInstance, AxiosRequestConfig } from 'axios';
import { Configuration } from '../configuration';
// Some imports not used depending on template conditions
// @ts-ignore
import { DUMMY_BASE_URL, assertParamExists, setApiKeyToObject, setBasicAuthToObject, setBearerAuthToObject, setOAuthToObject, setSearchParams, serializeDataIfNeeded, toPathString, createRequestFunction } from '../common';
// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS, RequestArgs, BaseAPI, RequiredError } from '../base';
// @ts-ignore
import { BearerResponse } from '../models';
// @ts-ignore
import { ErrorModel } from '../models';
// @ts-ignore
import { HTTPValidationError } from '../models';
// @ts-ignore
import { UserCreate } from '../models';
// @ts-ignore
import { UserRead } from '../models';
/**
 * AuthApi - axios parameter creator
 * @export
 */
export const AuthApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * 
         * @summary Auth:Jwt.Login
         * @param {string} username 
         * @param {string} password 
         * @param {string} [grantType] 
         * @param {string} [scope] 
         * @param {string} [clientId] 
         * @param {string} [clientSecret] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        authJwtLogin: async (username: string, password: string, grantType?: string, scope?: string, clientId?: string, clientSecret?: string, options: AxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'username' is not null or undefined
            assertParamExists('authJwtLogin', 'username', username)
            // verify required parameter 'password' is not null or undefined
            assertParamExists('authJwtLogin', 'password', password)
            const localVarPath = `/api/v1/auth/jwt/login`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;
            const localVarFormParams = new URLSearchParams();


            if (grantType !== undefined) { 
                localVarFormParams.set('grant_type', grantType as any);
            }
    
            if (username !== undefined) { 
                localVarFormParams.set('username', username as any);
            }
    
            if (password !== undefined) { 
                localVarFormParams.set('password', password as any);
            }
    
            if (scope !== undefined) { 
                localVarFormParams.set('scope', scope as any);
            }
    
            if (clientId !== undefined) { 
                localVarFormParams.set('client_id', clientId as any);
            }
    
            if (clientSecret !== undefined) { 
                localVarFormParams.set('client_secret', clientSecret as any);
            }
    
    
            localVarHeaderParameter['Content-Type'] = 'application/x-www-form-urlencoded';
    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = localVarFormParams.toString();

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Auth:Jwt.Logout
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        authJwtLogout: async (options: AxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/auth/jwt/logout`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Register:Register
         * @param {UserCreate} userCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        registerRegister: async (userCreate: UserCreate, options: AxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'userCreate' is not null or undefined
            assertParamExists('registerRegister', 'userCreate', userCreate)
            const localVarPath = `/api/v1/auth/register`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(userCreate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * AuthApi - functional programming interface
 * @export
 */
export const AuthApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = AuthApiAxiosParamCreator(configuration)
    return {
        /**
         * 
         * @summary Auth:Jwt.Login
         * @param {string} username 
         * @param {string} password 
         * @param {string} [grantType] 
         * @param {string} [scope] 
         * @param {string} [clientId] 
         * @param {string} [clientSecret] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async authJwtLogin(username: string, password: string, grantType?: string, scope?: string, clientId?: string, clientSecret?: string, options?: AxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<BearerResponse>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.authJwtLogin(username, password, grantType, scope, clientId, clientSecret, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * 
         * @summary Auth:Jwt.Logout
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async authJwtLogout(options?: AxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<any>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.authJwtLogout(options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * 
         * @summary Register:Register
         * @param {UserCreate} userCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async registerRegister(userCreate: UserCreate, options?: AxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<UserRead>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.registerRegister(userCreate, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
    }
};

/**
 * AuthApi - factory interface
 * @export
 */
export const AuthApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = AuthApiFp(configuration)
    return {
        /**
         * 
         * @summary Auth:Jwt.Login
         * @param {string} username 
         * @param {string} password 
         * @param {string} [grantType] 
         * @param {string} [scope] 
         * @param {string} [clientId] 
         * @param {string} [clientSecret] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        authJwtLogin(username: string, password: string, grantType?: string, scope?: string, clientId?: string, clientSecret?: string, options?: any): AxiosPromise<BearerResponse> {
            return localVarFp.authJwtLogin(username, password, grantType, scope, clientId, clientSecret, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Auth:Jwt.Logout
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        authJwtLogout(options?: any): AxiosPromise<any> {
            return localVarFp.authJwtLogout(options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Register:Register
         * @param {UserCreate} userCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        registerRegister(userCreate: UserCreate, options?: any): AxiosPromise<UserRead> {
            return localVarFp.registerRegister(userCreate, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * Request parameters for authJwtLogin operation in AuthApi.
 * @export
 * @interface AuthApiAuthJwtLoginRequest
 */
export interface AuthApiAuthJwtLoginRequest {
    /**
     * 
     * @type {string}
     * @memberof AuthApiAuthJwtLogin
     */
    readonly username: string

    /**
     * 
     * @type {string}
     * @memberof AuthApiAuthJwtLogin
     */
    readonly password: string

    /**
     * 
     * @type {string}
     * @memberof AuthApiAuthJwtLogin
     */
    readonly grantType?: string

    /**
     * 
     * @type {string}
     * @memberof AuthApiAuthJwtLogin
     */
    readonly scope?: string

    /**
     * 
     * @type {string}
     * @memberof AuthApiAuthJwtLogin
     */
    readonly clientId?: string

    /**
     * 
     * @type {string}
     * @memberof AuthApiAuthJwtLogin
     */
    readonly clientSecret?: string
}

/**
 * Request parameters for registerRegister operation in AuthApi.
 * @export
 * @interface AuthApiRegisterRegisterRequest
 */
export interface AuthApiRegisterRegisterRequest {
    /**
     * 
     * @type {UserCreate}
     * @memberof AuthApiRegisterRegister
     */
    readonly userCreate: UserCreate
}

/**
 * AuthApi - object-oriented interface
 * @export
 * @class AuthApi
 * @extends {BaseAPI}
 */
export class AuthApi extends BaseAPI {
    /**
     * 
     * @summary Auth:Jwt.Login
     * @param {AuthApiAuthJwtLoginRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof AuthApi
     */
    public authJwtLogin(requestParameters: AuthApiAuthJwtLoginRequest, options?: AxiosRequestConfig) {
        return AuthApiFp(this.configuration).authJwtLogin(requestParameters.username, requestParameters.password, requestParameters.grantType, requestParameters.scope, requestParameters.clientId, requestParameters.clientSecret, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Auth:Jwt.Logout
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof AuthApi
     */
    public authJwtLogout(options?: AxiosRequestConfig) {
        return AuthApiFp(this.configuration).authJwtLogout(options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Register:Register
     * @param {AuthApiRegisterRegisterRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof AuthApi
     */
    public registerRegister(requestParameters: AuthApiRegisterRegisterRequest, options?: AxiosRequestConfig) {
        return AuthApiFp(this.configuration).registerRegister(requestParameters.userCreate, options).then((request) => request(this.axios, this.basePath));
    }
}
