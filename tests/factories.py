# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Reason, RecommendationModel



class RecFactory(factory.Factory):
    """Creates fake recommendations"""


    class Meta:
        model = RecommendationModel

    id = factory.Sequence(lambda n: n)
    
    name = factory.Faker("first_name")
    original_product_id = factory.Sequence(lambda n: n)

    recommendation_product_name = factory.Faker("first_name")
    recommendation_product_id = factory.Sequence(lambda n: n)

    reason = FuzzyChoice(choices=[Reason.CROSS_SELL , Reason.UP_SELL , Reason.ACCESSORY, Reason.OTHER])
