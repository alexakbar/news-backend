<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Api\BaseController as BaseController;
use App\Models\News;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use jcobhams\NewsApi\NewsApi;
use Illuminate\Support\Facades\Auth;


class ArticlesController extends BaseController
{

    /**
     * search articles
     *
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function searchArticles(Request $request): JsonResponse
    {
        // get search keyword
        $query = $request->q;
        // get filter inputs
        $filterCategories = $request->categories;
        $filterStartDate = $request->start_date;
        $filterEndDate = $request->end_date;
        $filterSources = $request->sources;

        $posts = News::query();

        // serach by keyword
        if ($query) {
            $posts->where(function ($q) use ($query) {
                $q->where('title', 'LIKE', "%$query%")
                    ->orWhere('description', 'LIKE', "%$query%");
            });
        }

        // filter categories
        if ($filterCategories) {
            $posts->whereIn('category', $filterCategories);
        }

        // filter start date
        if ($filterStartDate) {
            $posts->whereDate('published_at', '>=', $filterStartDate);
        }

        // filter end date
        if ($filterEndDate) {
            $posts->whereDate('published_at', '<=', $filterEndDate);
        }

        // filter prefred sources
        if ($filterSources) {
            $posts->whereIn('source', $filterSources);
        }

        // order by personal preference
        if (!empty(request()->user()) && empty($query) && empty($filterCategories) && empty($filterStartDate) && empty($filterEndDate) && empty($filterSources)) {
            // get user 
            $user = Auth::user();
            // get user authors
            $authors = json_decode($user->authors,true);
            // get user categories
            $categories = json_decode($user->categories,true);
            // get user preferred sources
            $preferredSources = json_decode($user->preferred_sources,true);

            
            // order by user preferred sources
            if ($preferredSources) {
                $posts->orderByRaw('FIELD(source, "' . implode('","', $preferredSources) . '") desc');
            }
            // order by user authors
            if ($authors) {
                $posts->orderByRaw('FIELD(author, "' . implode('","', $authors) . '") desc');
            }
            // order by user categories
            if ($categories) {
                $posts->orderByRaw('FIELD(category, "' . implode('","', $categories) . '") desc');
            }
            
        }

        $results = $posts->get();

        return $this->sendResponse($results->toArray(), 'Articles retrieved successfully.');
    }
}
