<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Api\BaseController as BaseController;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Validator;

class AuthController extends BaseController
{
    /**
     * Registration API
     * 
     * @return \Illuminate\Http\JsonResponse
     */

    public function register(Request $request): JsonResponse{
        
        $validator = Validator::make($request->all(), [
            'username' => 'required',
            'email' => 'required|unique:users|email',
            'password' => 'required',
            'c_password' => 'required|same:password',
        ]);

        if($validator->fails()){
            return $this->sendError('Validation Error.', $validator->errors());
        }

        // create user
        $input = $request->all();
        $input['password'] = bcrypt($input['password']);
        $user = User::create($input);

        $data = [];
        // create token
        $dataUser['username'] =  $user->username;
        $dataUser['email'] =  $user->email;
        $dataUser['is_personalized'] = false;
        $data['token'] = $user->createToken('Token')->accessToken;
        $data['data'] = $dataUser;

        return $this->sendResponse($data, 'User register successfully.', 201);
    }
    
    /**
     * Login API
     * 
     * @return \Illuminate\Http\JsonResponse
     */
    public function login(Request $request): JsonResponse
    {
        // check validation
        $validator = Validator::make($request->all(), [
            'email' => 'required|email',
            'password' => 'required',
        ]);

        if($validator->fails()){
            return $this->sendError('Validation Error.', $validator->errors());
        }

        // check email and password
        if(Auth::attempt(['email' => $request->email, 'password' => $request->password])){ 
            $user = User::where('email', $request->email)->first();
            $data = [];
            $data['token'] = $user->createToken('Token')->accessToken;
            $dataUser['username'] =  $user->username;
            $dataUser['email'] =  $user->email;
            $dataUser['is_personalized'] = $user->is_personalized ? true : false;
            $data['data'] = $dataUser;

            return $this->sendResponse($data, 'User login successfully.');
        } 
        else{ 
            return $this->sendError('Unauthorised.', ['error' => 'Unauthorised']);
        } 
    }

    /**
     * Logout API
     * 
     * @return \Illuminate\Http\JsonResponse
     */
    public function logout(Request $request): JsonResponse
    {
        // check validation
        $validator = Validator::make($request->all(), [
            'token' => 'required',
        ]);

        if($validator->fails()){
            return $this->sendError('Validation Error.', $validator->errors());
        }

        // check token
        if ($request->user()->token()->revoke()){
            return $this->sendResponse([], 'User logout successfully.');
        } else{
            return $this->sendError('Unauthorised.', ['error' => 'Unauthorised']);
        }
    }
    
}
