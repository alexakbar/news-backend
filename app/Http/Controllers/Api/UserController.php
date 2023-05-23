<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Api\BaseController as BaseController;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class UserController extends BaseController
{
    /**
     * get user
     * 
     * @return \Illuminate\Http\JsonResponse
     */
    public function getUser(): JsonResponse
    {
        // get user 
        $user = Auth::user();
        return $this->sendResponse($user, 'User retrieved successfully.');
    }

    /**
     * set personalize user 
     * 
     * @return \Illuminate\Http\JsonResponse
     */
    public function setPersonalize(Request $request): JsonResponse
    {
        // get user 
        $user = Auth::user();

        // update user author, category, source
        $user = User::find($user->id);
        if ($request->authors != null) {
            if(is_array($request->authors)){
                // array to json 
                $user->authors = json_encode($request->authors);
            }
        }
        if ($request->categories != null) {
            if(is_array($request->categories)){
                // array to json 
                $user->categories = json_encode($request->categories);
            }
        }
        if ($request->preferred_sources != null) {
            if(is_array($request->preferred_sources)){
                // array to json 
                $user->preferred_sources = json_encode($request->preferred_sources);
            }
        }

        // check not is_personalized
        if (!$user->is_personalized) {
            $user->is_personalized = true;
        }

        $user->save();

        return $this->sendResponse($user, 'User retrieved successfully.');
    }
}
